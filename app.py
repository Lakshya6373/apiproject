import os
import random
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

# --- Configuration ---
API_TOKEN = os.getenv('API_TOKEN')
# The counter file will be stored on a persistent disk at this path
COUNTER_FILE = '/var/data/counter.txt'
# A lock to prevent race conditions
counter_lock = threading.Lock()

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

    # --- Generate Sequential Number ---
    with counter_lock:
        try:
            with open(COUNTER_FILE, 'r') as f:
                current_number = int(f.read())
        except (FileNotFoundError, ValueError):
            # If the file doesn't exist or is empty, start at 1000
            current_number = 1000
        
        next_number = current_number + 1
        
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(next_number))

    # The JSON key is now 'sequential_number' for clarity
    return jsonify(sequential_number=next_number)
