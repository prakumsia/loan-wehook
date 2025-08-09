from flask import Flask, request, jsonify
import logging

# Initialize the Flask app
app = Flask(__name__)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return "✅ Loan Webhook is deployed and running."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log the incoming request for debugging purposes
        req = request.get_json()
        logging.debug("📥 Received request:")
        logging.debug(req)

        # Extract parameters from the incoming request
        parameters = req.get("sessionInfo", {}).get("parameters", {})
        tag = req.get("fulfillmentInfo", {}).get("tag", "")
        logging.debug(f"🔖 Triggered by tag: {tag}")

        # Extract values from the parameters with defaults if not present
        loan_type = parameters.get("loan_type", "not given")
        age = parameters.get("age", "not given")
        income = parameters.get("monthly_income", "not given")
        employment = parameters.get("employment_type", "not given")
        credit_score = parameters.get("credit_score", "not given")
        existing_emi = parameters.get("existing_emi", "not given")

        # Function to format values as currency
        def format_currency(value):
            try:
                return f"₹{int(value):,}"
            except ValueError:
                return "₹not given"

        # Format income and existing EMI as currency
        income = format_currency(income)
        existing_emi = format_currency(existing_emi)

        # Compose the response message
        offer_message = (
            f"We received your application for a {loan_type} loan. "
            f"Profile: Age {age}, Income {income}, Employment: {employment}, "
            f"Credit Score: {credit_score}, EMI: {existing_emi}."
        )

        # Return the response to the caller (e.g., Dialogflow, etc.)
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
        # Log any errors that occur
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

# Run the app with debug mode enabled and accessible externally
if __name__ == "__main__":
    logging.debug("Starting Flask application in debug mode...")
    app.run(debug=True, host="0.0.0.0", port=8080)
