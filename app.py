#app.py
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

LOG_FILE = "log.json"

# 初期データ
latest_data = {
    "ds": None,
    "pico": None,
    "time": "--:--:--"
}

# ログ読み込み
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_data = json.load(f)
else:
    log_data = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def receive():
    global latest_data, log_data

    data = request.json

    # UTC → 日本時間
    jst = datetime.utcnow() + timedelta(hours=9)
    data["time"] = jst.strftime("%H:%M:%S")
    
    latest_data = data

    # ログ追加
    log_data.append(data)

    # 最大100件
    if len(log_data) > 100:
        log_data.pop(0)

    # JSON保存
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False)

    print("受信:", data)
    return "OK"

@app.route("/get")
def get_data():
    return jsonify(latest_data)

@app.route("/log")
def get_log():
    return jsonify(log_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
