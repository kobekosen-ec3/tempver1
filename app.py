#app.py
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
latest_data = { }

# GASのURLに変更
GAS_URL = "https://script.google.com/macros/s/AKfycbw4jSdZjcgoTG2CILDIHX2mE93l38f3SVwGyUm5k5FYHn9zIIF1IlCr_eeH9NebvyV4qQ/exec"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def receive():
    global latest_data
    data = request.json
    device_id = data.get("device_id")
    if device_id:
        latest_data[device_id] = data
    try:
        requests.post(GAS_URL, json=data)
    except:
        pass
    return "OK"

@app.route("/devices")
def devices():
    return jsonify(latest_data)

@app.route("/get")
def get_data():
    return jsonify(latest_data)

@app.route("/log")
def get_log():
    try:
        res = requests.get(GAS_URL)
        print(res.text)
        return res.text, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print("log error:", e)
        return "[]"

@app.route("/discord")
def discord():
    return render_template("discord.html")
    
discord_webhook = ""
@app.route("/discord_setting", methods=["POST", "GET"])
def discord_setting():
    global discord_webhook
    if request.method == "POST":
        data = request.get_json()
        discord_webhook = data["webhook"]
        requests.post(
            GAS_URL,
            json={
                "mode": "setWebhook",
                "webhook": discord_webhook
            }
        )
        return jsonify({"status": "ok"})
    return jsonify({
        "webhook": discord_webhook
    })
    
@app.route("/discord_test", methods=["POST"])
def discord_test():
    global discord_webhook
    if discord_webhook == "":
        return "Webhook未設定", 400
    payload = {
        "username": "温度管理BOT",
        "avatar_url": "https://raw.githubusercontent.com/kobekosen-ec3/imgpublic/main/tempBOT.png",
        "content": "✅ テスト通知です"
    }
    res = requests.post(discord_webhook, json=payload)
    return jsonify({
        "status": res.status_code
    })

threshold = 30.0
@app.route("/threshold", methods=["GET", "POST"])
def threshold_api():
    global threshold
    if request.method == "POST":
        data = request.get_json()
        threshold = float(data["threshold"])
        return jsonify({"status": "ok"})
    return jsonify({"threshold": threshold})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
