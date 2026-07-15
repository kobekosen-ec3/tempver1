#app.py
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
latest_data = { }

# GASのURLに変更
GAS_URL = "https://script.google.com/macros/s/AKfycbx8nKHF0gFDZuy33tlMlYNpBhCh80DDPyq5RK7jRD9Uk-P4zpvHI2WbBN6fsMAG4MEcGQ/exec"

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

@app.route("/line")
def line():
    return render_template("discord.html")
    

@app.route("/discord_setting", methods=["GET", "POST"])
def discord_setting():

    if request.method == "POST":
        data = request.get_json()
        requests.post(
            GAS_URL,
            json={
                "mode": "setWebhook",
                "webhook": data["webhook"]
            }
        )
        return jsonify({"status": "ok"})

    res = requests.get(GAS_URL, params={"mode": "getWebhook"})
    return jsonify(res.json())

@app.route("/discord_test", methods=["POST"])
def discord_test():
    requests.post(
        GAS_URL,
        json={
            "mode": "testDiscord"
        }
    )
    return jsonify({"status": "ok"})

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
