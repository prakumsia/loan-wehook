
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Loan Webhook!"

# Loan inquiry route (POST)
@app.route('/loan', methods=['POST'])
def loan_inquiry():
    # Get data from request
    data = request.get_json()
    
    # Example loan logic
    loan_amount = data.get('loan_amount', 0)
    loan_years = data.get('loan_years', 0)
    
    if loan_amount and loan_years:
        # Just an example logic: calculate the interest
        interest_rate = 0.1  # 10% interest rate
        total_payment = loan_amount * (1 + interest_rate * loan_years)
        monthly_payment = total_payment / (loan_years * 12)
        
        return jsonify({
            "message": f"Loan amount of {loan_amount} for {loan_years} years will have a monthly payment of {monthly_payment:.2f}. Total payment: {total_payment:.2f}."
        })
    else:
        return jsonify({
            "message": "Please provide both loan amount and loan years."
        })

if __name__ == '__main__':
    # Get the port from the environment variable or default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug to False for production
