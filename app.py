from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("📥 Incoming request:")
    print(req)

    # Get parameters from sessionInfo
    parameters = req.get("sessionInfo", {}).get("parameters", {})

    # Optional: Get the tag that triggered this webhook
    tag = req.get("fulfillmentInfo", {}).get("tag", "")
    print(f"🔖 Triggered by tag: {tag}")

    # Extract user data
    loan_type = parameters.get("loan_type", "unknown loan")
    age = parameters.get("age")
    income = parameters.get("monthly_income")
    employment = parameters.get("employment_type")
    credit_score = parameters.get("credit_score")
    existing_emi = parameters.get("existing_emi")

    # Simulate business logic (replace with actual offer calc or API call)
    offer_message = f"We’ve received your application for a {loan_type}. Based on your profile (income: ₹{income}, credit score: {credit_score}), we’ll now generate offers."

    # Respond to Dialogflow CX
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
