from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("📥 Incoming request:")
    print(req)

    # Get parameters safely
    parameters = req.get("sessionInfo", {}).get("parameters", {})
    tag = req.get("fulfillmentInfo", {}).get("tag", "")
    print(f"🔖 Triggered by tag: {tag}")

    # Extract and log parameters
    loan_type = parameters.get("loan_type", "not given")
    age = parameters.get("age", "not given")
    income = parameters.get("monthly_income", "not given")
    employment = parameters.get("employment_type", "not given")
    credit_score = parameters.get("credit_score", "not given")
    existing_emi = parameters.get("existing_emi", "not given")

    # Build safe response
    offer_message = (
        f"We received your application for a {loan_type} loan. "
        f"Profile: Age {age}, Income ₹{income}, Employment: {employment}, "
        f"Credit Score: {credit_score}, EMI: ₹{existing_emi}."
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
