from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route("/", methods=["POST"])
def chat():
    try:
        data = request.json
        headers = {
            "Authorization": request.headers.get("Authorization"),
            "Content-Type": "application/json"
        }
        response = requests.post(OPENAI_API_URL, json=data, headers=headers)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
