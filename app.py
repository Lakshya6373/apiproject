import os
import random
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

# --- Configuration ---
API_TOKEN = os.getenv('API_TOKEN')
COUNTER_FILE = '/var/data/counter.txt'
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

    # --- Simplified Sequential Number Logic ---
    with counter_lock:
        try:
            # Try to read the last number from the file.
            with open(COUNTER_FILE, 'r') as f:
                current_number = int(f.read())
        except (FileNotFoundError, ValueError):
            # If the file doesn't exist or is empty, this is the first run.
            # We'll start the sequence at 1000.
            current_number = 1000
        
        next_number = current_number + 1
        
        # Write the new number back to the file.
        # The 'w' mode will create the file if it doesn't exist.
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(next_number))

    return jsonify(sequential_number=next_number)
