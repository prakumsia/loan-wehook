from flask import Flask, request, jsonify
import logging
import requests  # Import the requests library for making HTTP requests

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Loan Webhook is deployed and running."

@app.route('/check-ip')
def check_ip():
    try:
        # Fetch the public IP of the server from httpbin.org
        response = requests.get('https://httpbin.org/ip')
        return jsonify(response.json())  # Return the response as JSON
    except Exception as e:
        logging.error(f"❌ Error fetching IP: {e}")
        return jsonify({
            "message": "Failed to fetch IP"
        })

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        logging.info("📥 Received request:")
        logging.info(req)

        # Get parameters safely from the incoming request
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

        # Compose a response message with the extracted data
        offer_message = (
            f"We received your application for a {loan_type} loan. "
            f"Profile: Age {age}, Income ₹{income}, Employment: {employment}, "
            f"Credit Score: {credit_score}, EMI: ₹{existing_emi}."
        )

        # Send the response back in the required format
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
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
    app.run(debug=True, host="0.0.0.0", port=8080)  # Run the app on port 8080
