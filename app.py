#app.py
from flask import Flask, request, jsonify, render_template
import requests


app = Flask(__name__)

latest_data = {
    "ds": None,
    "pico": None,
    "time": "--"
}

# GASのURLに変更
GAS_URL = "https://script.google.com/macros/s/AKfycbz2zaEWHde2jAPECg80vL9zpWWfh-rl4cbGDwu4w6lbj6zIkFUSK34mqWU-3-WHJdTTdA/exec"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def receive():
    global latest_data

    data = request.json
    latest_data = data

    # GASへ転送
    try:
        requests.post(GAS_URL, json=data)
    except:
        pass

    return "OK"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
