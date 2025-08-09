from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Loan Webhook is deployed and running."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        logging.info("📥 Received request:")
        logging.info(req)

        # Get parameters safely
        parameters = req.get("sessionInfo", {}).get("parameters", {})
        tag = req.get("fulfillmentInfo", {}).get("tag", "")
        logging.info(f"🔖 Triggered by tag: {tag}")

        # Extract parameters with defaults
        loan_type = parameters.get("loan_type", "not given")
        age = parameters.get("age", "not given")
        income = parameters.get("monthly_income", "not given")
        employment = parameters.get("employment_type", "not given")
        credit_score = parameters.get("credit_score", "not given")
        existing_emi = parameters.get("existing_emi", "not given")

        # Ensure that income and existing_emi are in the correct format for the response
        try:
            income = f"₹{int(income):,}"
        except ValueError:
            income = "₹not given"

        try:
            existing_emi = f"₹{int(existing_emi):,}"
        except ValueError:
            existing_emi = "₹not given"

        # Compose response message
        offer_message = (
            f"We received your application for a {loan_type} loan. "
            f"Profile: Age {age}, Income {income}, Employment: {employment}, "
            f"Credit Score: {credit_score}, EMI: {existing_emi}."
        )

        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [offer_message]
                        }
                    }
                ]
            }
        })

    except Exception as e:
        logging.error(f"❌ Exception occurred: {e}")
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": ["An error occurred while processing your loan application. Please try again later."]
                        }
                    }
                ]
            }
        })

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host="0.0.0.0", port=8080)
