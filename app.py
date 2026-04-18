from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

latest_data = {
    "ds": None,
    "pico": None,
    "time": "--:--:--"
}

@app.route("/")
def home():
    return render_template("index.html")  # ← ここ変更

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
