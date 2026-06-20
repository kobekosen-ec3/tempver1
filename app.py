#app.py
from flask import Flask, request, jsonify, render_template
import requests


app = Flask(__name__)

# latest_data = {
#     "ds": None,
#     "pico": None,
#     "time": "--",
#     "device":None
# }
latest_data = { }

# GASのURLに変更
GAS_URL = "https://script.google.com/macros/s/AKfycbw4jSdZjcgoTG2CILDIHX2mE93l38f3SVwGyUm5k5FYHn9zIIF1IlCr_eeH9NebvyV4qQ/exec"


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/data", methods=["POST"])
# def receive():
#     global latest_data

#     data = request.json
#     latest_data = data

#     # GASへ転送
#     try:
#         requests.post(GAS_URL, json=data)
#     except:
#         pass

#     return "OK"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
