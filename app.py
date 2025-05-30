import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Loan Webhook is live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("Received request:", req)
    # Sample response
    return jsonify({"fulfillmentText": "Webhook response from Cloud Run!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)