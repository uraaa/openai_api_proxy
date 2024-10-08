import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
BASE_URL = "https://api.openai.com"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route("/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('Authorization')
    }

    response = requests.request(
        url=url,
        method=request.method,
        data=request.json,
        headers=headers
    )

    return response.json()


if __name__ == "__main__":
    app.run()
