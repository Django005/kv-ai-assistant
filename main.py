from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RASA_CALM_API_URL = "http://localhost:5005"

@app.route("/prompt", methods=["POST"])
def prompt():
    data = request.get_json()
    user_cookies = request.cookies.to_dict()

    xcsrf_token = user_cookies.get("x-csrf-token")
    user_cookies_str = '; '.join(f'{key}={value}' for key, value in user_cookies.items())
    language = user_cookies.get("kvsLanguage").split("-")[0] # get language preference of user
    payload = {
        "sender": data.get("sender"),
        "message": data.get("message"),
        "metadata": {
            "cookies": user_cookies_str,
            "X-Csrf-Token": xcsrf_token,
            "language": language
        }
    }
    
    try:
        response = requests.post(RASA_CALM_API_URL + "/webhooks/rest/webhook", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return jsonify({"message": str(e)}), 500

    # placeholder for testing purposes
    # return [
    #     {
    #         "recipient_id": "demouser123",
    #         "text": "Backend systems not funcional. Please try again later..."
    #     }
    # ]

if __name__ == "__main__":
    app.run(debug=True)