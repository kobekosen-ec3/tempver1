from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

latest_data = {
    "ds": None,
    "pico": None,
    "time": "--:--:--"
}

# 👇 ここ変更
@app.route("/")
def home():
    return send_file("index.html")

@app.route("/data", methods=["POST"])
def receive():
    global latest_data
    latest_data = request.json
    print("受信:", latest_data)
    return "OK"

@app.route("/get", methods=["GET"])
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
