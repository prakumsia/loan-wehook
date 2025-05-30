from flask import Flask, request, jsonify
from utils import check_loan_eligibility

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_params = data.get("sessionInfo", {}).get("parameters", {})
    response_text = check_loan_eligibility(user_params)
    return jsonify({"fulfillment_response": {"messages": [{"text": {"text": [response_text]}}]}})

if __name__ == "__main__":
    app.run(debug=True)
