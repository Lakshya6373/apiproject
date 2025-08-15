import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Configuration ---
API_TOKEN = os.getenv('API_TOKEN')

@app.route('/api/random-number', methods=['GET'])
def get_number():
    # --- Security Check ---
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify(error="Unauthorized: Missing or invalid token"), 401

    provided_token = auth_header.split(' ')[1]
    if not API_TOKEN:
         return jsonify(error="Server error: API_TOKEN not configured"), 500
    if provided_token != API_TOKEN:
        return jsonify(error="Unauthorized: Invalid token"), 401

    # --- NEW: Generate a sequential number from the current time ---
    # This gets the number of seconds since 1970 and takes the last 5 digits.
    # It will be unique and sequential for every request.
    random_number = int(time.time()) % 100000
    
    return jsonify(sequential_number=sequential_number)
