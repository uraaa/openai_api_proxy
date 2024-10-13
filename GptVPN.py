import logging
import os
from flask import Flask, request, jsonify, Response
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OPENAI_URL = "https://api.openai.com"
PROXY_AUTH_KEY = os.getenv('PROXY_AUTH_KEY')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route("/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(endpoint):
    # check proxy auth
    if request.headers.get('X-PROXY-AUTH-KEY') != PROXY_AUTH_KEY:
        return jsonify('Unauthorized'), 401

    # prepare data
    url = f"{OPENAI_URL}/{endpoint}"
    headers = {
        'Authorization': request.headers.get('Authorization'),
    }

    # get response from openai
    response = requests.request(
        url=url,
        method=request.method,
        json=request.json,
        headers=headers,
    )

    # Extract important headers
    response_headers = []
    meta_headers = [
        'openai-organization', 'openai-processing-ms', 'openai-version', 'x-request-id',
        'x-ratelimit-limit-requests', 'x-ratelimit-limit-tokens', 'x-ratelimit-remaining-requests',
        'x-ratelimit-remaining-tokens', 'x-ratelimit-reset-requests', 'x-ratelimit-reset-tokens'
    ]

    for header in meta_headers:
        if response.headers.get(header):
            response_headers.append((header, response.headers.get(header)))

    return Response(response.content, response.status_code, response_headers)


if __name__ == "__main__":
    app.run()
