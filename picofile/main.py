#main.py
import time

from network import (
    WLAN,
    STA_IF,
    STAT_GOT_IP,
    STAT_NO_AP_FOUND,
    STAT_CONNECT_FAIL,
    STAT_WRONG_PASSWORD,
)
from machine import reset

from wifi_setup import WifiConfig, WifiSetupPortal

class IoTDevice:
    def execute(self) -> None:
        try:
            if not WifiConfig().check():
                print("start wifi setup portal")
                WifiSetupPortal().execute()
            else:
                print("start iot device")
                if not self._connect_wifi():
                    raise Exception("cannot connect wifi")
                self._main_routine()
        except Exception as e:
            print(f"{e=}")
            time.sleep(1)
            reset()

    def _connect_wifi(self) -> bool:
        ssid: str
        key: str
        ssid, key = WifiConfig().get()
        
        print("SSID =", ssid)
        #print("KEY =", key)
        
        time.sleep(1)
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)
        print(self.wlan.scan())
        self.wlan.connect(ssid, key)

        while True:
            time.sleep(1)
            status = self.wlan.status()
            
            print("wifi status =", status)
            
            if status == STAT_NO_AP_FOUND or status == STAT_CONNECT_FAIL:
                break
            elif status == STAT_WRONG_PASSWORD:
                print("cannot connect wifi because incorrect password so wifi_config reset")
                WifiConfig().delete()
                reset()
                break
            elif status == STAT_GOT_IP:
                print("WiFi connected")
                return True
        return False

    def _main_routine(self) -> None:
        # Your main routine here
        print("main routine")
        
        import machine
        import socket
        import urequests
        from machine import Pin, ADC, RTC, PWM
        import onewire
        import ds18x20
        import binascii
        
        import network
        import ntptime
        import rp2
        
#         ntptime.host = "time.cloudflare.com"
#         
#         time.sleep(3)
# 
#         try:
#             ntptime.settime()
#             print("NTP時刻同期に成功しました")
#         except Exception as e:
#             print("NTP時刻同期に失敗しました")
#             print(e)

        ip = self.wlan.ifconfig()[0]
        print("Server started:", ip)
        
        
        
        def NTPset():
            ntptime.host = "ntp.nict.jp"

            # インターネット経由で現在時刻（UTC）を取得してRTCに設定
            for i in range(3):
                try:
                    ntptime.settime()
                    print("NTP時刻同期成功")
                    return True

                except Exception as e:
                    print("失敗", e)
                    time.sleep(1)

            print("NTP時刻同期に失敗しました")
            return False
        
        print(self.wlan.ifconfig())
        print(self.wlan.isconnected())
        
        NTPset()
            

        # センサー初期化
        sensor = ADC(4)
        rtc = RTC()
        led = Pin("LED", Pin.OUT)
        
        dat = Pin(4)
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(dat))
        roms = ds_sensor.scan()
        print("DS18B20:", roms)
        
        BUZZER_PIN = 15
        buzzer = PWM(Pin(BUZZER_PIN))

        # サーバー初期化
        URL = "https://temp-v2ms.onrender.com/data"
        THRESHOLD_URL = "https://temp-v2ms.onrender.com/threshold"
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        s.settimeout(1)

        print("Server started:", ip)
        last_beep_time = 0
        last_temp_time = 0

        buzzer_on = False
        beep_start_time = 0
        
        temp_conversion_running = False
        temp_start_time = 0

        ds_temp = None
        uid = str(binascii.hexlify(machine.unique_id()), "utf-8")
        
        pico_temp = 0
        day_str = "----/--/--"
        time_str = "--:--:--"
        threshold = 30.0
        

        def alarm(temp, threshold, frequency, duration):
            """
            指定した周波数と長さで音を鳴らします
            :param frequency: 音の周波数 (Hz)
            :param duration: 音の長さ (秒)
            """
            nonlocal buzzer_on, beep_start_time, last_beep_time
            if temp is None:
                return
            
            # ブザー開始
            if (not buzzer_on and temp >= threshold and time.ticks_diff(now, last_beep_time) >= 100):
                buzzer.freq(frequency)
                buzzer.duty_u16(32768)

                buzzer_on = True
                beep_start_time = now
                last_beep_time = now

            # duration秒経過したら停止
            if buzzer_on and time.ticks_diff(now, beep_start_time) >= duration:
                buzzer.duty_u16(0)
                buzzer_on = False
                
        while True:
            now = time.ticks_ms()

            # ---- 温度取得（10秒ごと）----
            if (not temp_conversion_running and time.ticks_diff(now, last_temp_time) >= 10000):
                if roms:
                    ds_sensor.convert_temp()
                    temp_conversion_running = True
                    temp_start_time = now
                    
            if (temp_conversion_running and
                time.ticks_diff(now, temp_start_time) >= 750):
        
                current_time = time.localtime(time.time() + 9 * 60 * 60)#時間取得

                ds_temp = ds_sensor.read_temp(roms[0])

                reading = sensor.read_u16()
                voltage = reading * 3.3 / 65535
                pico_temp = 27 - (voltage - 0.706) / 0.001721

                dt = rtc.datetime()
                day_str = f"{current_time[0]}/{current_time[1]:02d}/{current_time[2]:02d}"
                time_str = f"{current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}"
                
                print(f"[{time_str}] DS: {ds_temp}℃ / Pico: {pico_temp:.2f}℃")

                data = {
                    "device_id": uid,
#                     "product_id": "KOSEN-0001",
                    "ds": ds_temp,
                    "pico": pico_temp,
                    "time": time_str,
                    "day":day_str,
                    "threshold": threshold
                }

                try:
                    buzzer.duty_u16(0)
                    buzzer_on = False
                    print("送信中...")
                    res = urequests.post(URL, json=data)
                    print("POST終了")
                    print("ステータス:", res.status_code)
                    res.close()
                except Exception as e:
                    print("送信失敗:", e)
                    
                temp_conversion_running = False
                last_temp_time = now
                
                try:
                    res = urequests.get(THRESHOLD_URL)

                    print("status =", res.status_code)
                    print("body =", res.text)

                    threshold = float(res.json()["threshold"])
                    res.close()

                except Exception as e:
                    print("設定温度取得失敗:", e)
                    
                
                
                
            # ---- ブザー制御 ----
            alarm(ds_temp, threshold, 2000, 100)

            # ---- 通信処理 ----
            try:
                
                conn, addr = s.accept()
                print("Access from", addr)

                request = conn.recv(1024)

                response = f"""HTTP/1.1 200 OK
        Content-Type: application/json

        {{"ds": {ds_temp}, "pico": {pico_temp}, "time": "{time_str}"}}
        """
                conn.send(response)
                conn.close()

            except OSError:
                pass

if __name__ == "__main__":
    IoTDevice().execute()

