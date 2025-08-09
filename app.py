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

        # Get parameters directly from the request
        parameters = req.get("sessionInfo", {}).get("parameters", {})
        
        # Extract parameters safely
        loan_type = parameters.get("loan_type", "not provided")
        age = parameters.get("age", "not provided")
        income = parameters.get("monthly_income", "not provided")
        employment = parameters.get("employment_type", "not provided")
        credit_score = parameters.get("credit_score", "not provided")
        existing_emi = parameters.get("existing_emi", "not provided")

        # Compose the response message
        offer_message = (
            f"Loan Application received:\n"
            f"Loan Type: {loan_type}\n"
            f"Age: {age}\n"
            f"Monthly Income: ₹{income}\n"
            f"Employment: {employment}\n"
            f"Credit Score: {credit_score}\n"
            f"Existing EMI: ₹{existing_emi}"
        )

        # Return the response directly (no Dialogflow-specific structure)
        return jsonify({
            "message": offer_message
        })

    except Exception as e:
        logging.error(f"❌ Error processing request: {e}")
        return jsonify({
            "message": f"An error occurred: {str(e)}. Please try again later."
        })

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host="0.0.0.0", port=8080)
