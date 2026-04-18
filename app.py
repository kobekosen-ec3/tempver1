from flask import Flask, request, render_template

app = Flask(__name__)

# 最新データを保存
latest_data = {
    "ds": "--",
    "pico": "--",
    "time": "--"
}

# ホーム（スマホ表示）
@app.route("/")
def home():
    return render_template("index.html", data=latest_data)

# データ受信
@app.route("/data", methods=["POST"])
def receive():
    global latest_data
    latest_data = request.json
    print("受信:", latest_data)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
