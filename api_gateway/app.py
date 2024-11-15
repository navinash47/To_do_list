from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from functools import wraps
import jwt
from dotenv import load_dotenv

load_dotenv()

app = create_app()

# Service URLs
AUTH_SERVICE_URL = 'http://localhost:5001'
TASK_SERVICE_URL = 'http://localhost:5002'
SUGGESTION_SERVICE_URL = 'http://localhost:5003'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split()[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated

# Auth routes
@app.route('/auth/register', methods=['POST'])
def register():
    response = requests.post(f'{AUTH_SERVICE_URL}/register', json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/auth/login', methods=['POST'])
def login():
    response = requests.post(f'{AUTH_SERVICE_URL}/login', json=request.get_json())
    return jsonify(response.json()), response.status_code

# Task routes
@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    response = requests.post(f'{TASK_SERVICE_URL}/tasks', json=request.get_json())
    if response.status_code == 201:
        # Add to suggestions
        requests.post(f'{SUGGESTION_SERVICE_URL}/suggestions/add', 
                     json={'task_text': request.get_json().get('task_text')})
    return jsonify(response.json()), response.status_code

@app.route('/tasks/<user_id>', methods=['GET'])
@token_required
def get_tasks(user_id):
    response = requests.get(f'{TASK_SERVICE_URL}/tasks/{user_id}')
    return jsonify(response.json()), response.status_code

@app.route('/tasks/complete/<task_id>', methods=['PUT'])
@token_required
def complete_task(task_id):
    response = requests.put(f'{TASK_SERVICE_URL}/tasks/complete/{task_id}')
    return jsonify(response.json()), response.status_code

@app.route('/tasks/history/<user_id>', methods=['GET'])
@token_required
def get_task_history(user_id):
    response = requests.get(f'{TASK_SERVICE_URL}/tasks/history/{user_id}')
    return jsonify(response.json()), response.status_code

@app.route('/tasks/<task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    response = requests.put(f'{TASK_SERVICE_URL}/tasks/{task_id}', json=request.get_json())
    return jsonify(response.json()), response.status_code

# Suggestion routes
@app.route('/suggestions', methods=['GET'])
@token_required
def get_suggestions():
    response = requests.get(f'{SUGGESTION_SERVICE_URL}/suggestions', 
                          params={'q': request.args.get('q', '')})
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5000) 