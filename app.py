from flask import Flask, request, jsonify

app = Flask(__name__)

# 最新データを保存する変数
latest_data = {
    "ds": None,
    "pico": None,
    "time": "--:--:--"
}

# 確認用
@app.route("/")
def home():
    return "OK"

# データ受信（Pico → Render）
@app.route("/data", methods=["POST"])
def receive():
    global latest_data
    latest_data = request.json
    print("受信:", latest_data)
    return "OK"

# データ取得（スマホ → Render）
@app.route("/get", methods=["GET"])
def get_data():
    return jsonify(latest_data)

# Render用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
