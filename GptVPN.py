import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_OPENAI_API_KEY"  #Insert your own key

BASE_URL = "https://api.openai.com"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def build_headers(): #making default headers for automation
    client_headers = {key: value for key, value in request.headers if key != 'Host'}
    client_headers["Authorization"] = f"Bearer {API_KEY}"
    client_headers["Content-Type"] = "application/json"

    logging.info(f"Final request headers: {client_headers}")
    return client_headers


def get_request_data():
    data = request.get_json(silent=True)  # Getting JSON, if it is there
    logging.info(f"Request data: {data}")
    return data


def openai_response(response): #processing response from openAI
    logging.info(f"OpenAI API response status: {response.status_code}")
    logging.info(f"OpenAI API response headers: {response.headers}")
    logging.info(f"OpenAI API response body: {response.content}")
    return (response.content, response.status_code, dict(response.headers))


def send_request(url, method, headers, data=None):
    logging.info(f"Sending {method} request to {url}")

    if method == "GET":
        return requests.get(url, headers=headers, params=request.args)
    elif method == "POST":
        return requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        return requests.put(url, headers=headers, json=data)
    elif method == "DELETE":
        return requests.delete(url, headers=headers, json=data)
    elif method == "PATCH":
        return requests.patch(url, headers=headers, json=data)
    else:
        logging.error(f"Method {method} not allowed.")
        return jsonify({"error": f"Method {method} not allowed"}), 405


@app.route("/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy_request(endpoint):
    url = f"{BASE_URL}/{endpoint}"  # Making comlete URL
    headers = build_headers()  # Making header
    data = get_request_data()  # Gettin body
    response = send_request(url, request.method, headers, data)  #Sending rquest to OpenAI

    if isinstance(response, requests.Response):
        return openai_response(response)

    return response  #returns answer if request unsuccessful


if __name__ == "__main__":
    app.run()
