from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Loan Webhook is deployed and running."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log the raw request body to check what is being received
        raw_data = request.get_data(as_text=True)
        logging.info(f"📥 Received request body: {raw_data}")
        
        req = request.get_json()
        logging.info(f"📥 Decoded JSON: {req}")

        # Get parameters safely
        parameters = req.get("sessionInfo", {}).get("parameters", {})
        loan_type = parameters.get("loan_type", "not given")
        age = parameters.get("age", "not given")
        income = parameters.get("monthly_income", "not given")
        employment = parameters.get("employment_type", "not given")
        credit_score = parameters.get("credit_score", "not given")
        existing_emi = parameters.get("existing_emi", "not given")

        # Compose response message
        offer_message = (
            f"We received your application for a {loan_type} loan. "
            f"Profile: Age {age}, Income ₹{income}, Employment: {employment}, "
            f"Credit Score: {credit_score}, EMI: ₹{existing_emi}."
        )

        return jsonify({
            "message": offer_message
        })

    except Exception as e:
        logging.error(f"❌ Error processing request: {e}")
        return jsonify({
            "message": f"An error occurred while processing your loan application: {str(e)}. Please try again later."
        })

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host="0.0.0.0", port=8080)
