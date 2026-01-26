from flask import Flask, jsonify
import os

print("Starting Flask app...")


app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/hello")
def hello():
    return jsonify(
        message="Hello from Flask on GCP!",
        environment=os.getenv("ENV", "local")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
