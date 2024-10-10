import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OPENAI_URL = "https://api.openai.com"
PROXY_AUTH_KEY = '123'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route("/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(endpoint):

    # check proxy auth
    if request.headers.get('X-PROXY-AUTH-KEY') != PROXY_AUTH_KEY:
        return jsonify('Unauthorized'), 401

    # prepare data
    url = f"{OPENAI_URL}/{endpoint}"
    headers = {'Authorization': request.headers.get('Authorization')}

    # get response from openai
    response = requests.request(
        url=url,
        method=request.method,
        json=request.json,
        headers=headers
    )

    return response.json(), response.status_code

if __name__ == "__main__":
    app.run()
