import os
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# Securely load your secret token from an environment variable.
API_TOKEN = os.getenv('API_TOKEN')

@app.route('/api/random-number', methods=['GET'])
def get_random_number():
    # Security Check
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify(error="Unauthorized: Missing or invalid token"), 401

    provided_token = auth_header.split(' ')[1]

    if not API_TOKEN:
         return jsonify(error="Server error: API_TOKEN not configured"), 500

    if provided_token != API_TOKEN:
        return jsonify(error="Unauthorized: Invalid token"), 401

    # Generate Number (if authorized)
    random_number = random.randint(1000, 9999)
    return jsonify(random_number=random_number)
