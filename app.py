import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Add your routes and logic here...

if __name__ == '__main__':
    # Get the port from the environment variable or default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug to False for production
