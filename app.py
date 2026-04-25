from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

latest_data = {
    "ds": None,
    "pico": None,
    "time": "--:--:--"
}

# 👇 追加：ログ保存用
log_data = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def receive():
    global latest_data, log_data

    data = request.json
    latest_data = data

    # 👇 ログ追加（履歴保存）
    log_data.append(data)

    # 最大100件まで（重くならないように）
    if len(log_data) > 100:
        log_data.pop(0)

    print("受信:", data)
    return "OK"

# 最新データ
@app.route("/get")
def get_data():
    return jsonify(latest_data)

# 👇 履歴取得API
@app.route("/log")
def get_log():
    return jsonify(log_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
