from flask import Flask, request, jsonify
import logging, time, hmac, hashlib, base64, json, requests

# Initialize the Flask app
app = Flask(__name__)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# 🔑 BharatEVerify credentials
PARTNER_ID = "ESP00015"
API_TOKEN = "f0c63c79b863855fe6a41f97f50b380d8dc5d1d0"
API_URL = "https://api.bharateverify.com/api/v1/credit-bureau/get-score-only"

# ✅ Utility: Generate JWT
def create_jwt(partner_id, api_token):
    header = {"typ": "JWT", "alg": "HS256"}
    payload = {
        "partnerId": partner_id,
        "timestamp": int(time.time())
    }

    def b64url(data):
        return base64.urlsafe_b64encode(data).decode().replace("=", "")

    header_enc = b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_enc = b64url(json.dumps(payload, separators=(",", ":")).encode())

    signing_input = f"{header_enc}.{payload_enc}".encode()
    signature = hmac.new(api_token.encode(), signing_input, hashlib.sha256).digest()
    signature_enc = b64url(signature)

    return f"{header_enc}.{payload_enc}.{signature_enc}"

@app.route('/')
def index():
    return "✅ Loan Webhook is deployed and running."

# 📌 Webhook for Dialogflow CX or other bots
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        logging.debug("📥 Received request:")
        logging.debug(req)

        parameters = req.get("sessionInfo", {}).get("parameters", {})
        tag = req.get("fulfillmentInfo", {}).get("tag", "")
        logging.debug(f"🔖 Triggered by tag: {tag}")

        loan_type = parameters.get("loan_type", "not given")
        age = parameters.get("age", "not given")
        income = parameters.get("monthly_income", "not given")
        employment = parameters.get("employment_type", "not given")
        credit_score = parameters.get("credit_score", "not given")
        existing_emi = parameters.get("existing_emi", "not given")

        def format_currency(value):
            try:
                return f"₹{int(value):,}"
            except Exception:
                return "₹not given"

        income = format_currency(income)
        existing_emi = format_currency(existing_emi)

        offer_message = (
            f"We received your application for a {loan_type} loan. "
            f"Profile: Age {age}, Income {income}, Employment: {employment}, "
            f"Credit Score: {credit_score}, EMI: {existing_emi}."
        )

        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [offer_message]}}
                ]
            }
        })

    except Exception as e:
        logging.error(f"❌ Exception occurred: {e}")
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": ["An error occurred while processing your loan application. Please try again later."]}}
                ]
            }
        })

# 📌 New endpoint: BharatEVerify Credit Score
@app.route('/verify-score', methods=['POST'])
def verify_score():
    try:
        req_data = request.get_json(force=True)
        logging.debug(f"📥 Verify-Score Request: {req_data}")

        # Generate JWT
        jwt_token = create_jwt(PARTNER_ID, API_TOKEN)

        headers = {
            "Content-Type": "application/json",
            "Jwt-token": jwt_token
        }

        response = requests.post(API_URL, headers=headers, json=req_data, timeout=30)
        logging.debug(f"📤 BharatEVerify Response: {response.text}")

        return jsonify(response.json()), response.status_code

    except Exception as e:
        logging.error(f"❌ Error in /verify-score: {str(e)}")
        return jsonify({
            "status": False,
            "message": "Could not fetch credit score, please try again later.",
            "error": str(e)
        }), 500

# Run the app with debug mode enabled (Gunicorn will override this in production)
if __name__ == "__main__":
    logging.debug("Starting Flask application in debug mode...")
    app.run(debug=True, host="0.0.0.0", port=8080)
