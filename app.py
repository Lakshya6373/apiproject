import os
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Configuration ---
API_TOKEN = os.getenv('API_TOKEN')
REDIS_URL = os.getenv('REDIS_URL')

# --- Connect to Redis ---
try:
    redis_client = redis.from_url(REDIS_URL)
    # Set the counter to 1000 only if it doesn't already exist
    redis_client.setnx('api_counter', 1000)
except Exception as e:
    redis_client = None
    print(f"Could not connect to Redis: {e}")


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

    # --- Generate Sequential Number from Redis ---
    if not redis_client:
        return jsonify(error="Server error: Database connection failed"), 500

    # Atomically increment the counter and get the new value
    next_number = redis_client.incr('api_counter')
    
    return jsonify(sequential_number=next_number)
