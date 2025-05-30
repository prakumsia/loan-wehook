from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    tag = req['fulfillmentInfo']['tag']

    if tag == 'check_eligibility':
        return check_eligibility(req)
    elif tag == 'calculate_emi':
        return calculate_emi(req)
    elif tag == 'fetch_credit_score':
        return fetch_credit_score(req)
    else:
        return fallback_response()

def check_eligibility(req):
    session_params = req['sessionInfo']['parameters']
    age = int(session_params.get('age', 0))
    income = int(session_params.get('income', 0))
    employment = session_params.get('employment_type', '')

    if age < 21 or age > 60:
        message = "Sorry, you're not eligible. Age must be between 21 and 60."
    elif income < 20000:
        message = "Minimum income required is ₹20,000."
    else:
        message = f"You're eligible for a loan as a {employment} earning ₹{income}/month."

    return format_response(message)

def calculate_emi(req):
    params = req['sessionInfo']['parameters']
    P = float(params.get('loan_amount', 0))
    R = float(params.get('interest_rate', 10)) / 1200
    N = int(params.get('tenure_months', 12))

    emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
    emi = round(emi, 2)

    return format_response(f"Your monthly EMI will be ₹{emi}")

def fetch_credit_score(req):
    credit_score = 720
    return format_response(f"Your credit score is {credit_score}")

def fallback_response():
    return format_response("Sorry, I didn’t understand that.")

def format_response(msg):
    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [msg]}}]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)