from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
chat_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

@app.route("/", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    try:
        response = openai.ChatCompletion.create(
            model=chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        gpt_reply = response['choices'][0]['message']['content']
        return jsonify({"message": gpt_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
