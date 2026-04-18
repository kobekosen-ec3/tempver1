from flask import Flask, request

app = Flask(__name__)

# 確認用
@app.route("/")
def home():
    return "OK"

# データ受信
@app.route("/data", methods=["POST"])
def receive():
    data = request.json
    print("受信:", data)
    return "OK"

# Render用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
