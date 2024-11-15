from __init__ import create_app, token_required, handle_service_error
from flask import request, jsonify
import requests

app = create_app()

# Auth routes
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        response = requests.post(
            f"{app.config['AUTH_SERVICE_URL']}/register", 
            json=request.get_json()
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Auth service unavailable'}), 503

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        response = requests.post(
            f"{app.config['AUTH_SERVICE_URL']}/login", 
            json=request.get_json()
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Auth service unavailable'}), 503

# Task routes
@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    try:
        # Create task
        response = requests.post(
            f"{app.config['TASK_SERVICE_URL']}/tasks", 
            json=request.get_json()
        )
        
        if response.status_code == 201:
            # Add to suggestions
            requests.post(
                f"{app.config['SUGGESTION_SERVICE_URL']}/suggestions/add",
                json={'task_text': request.get_json().get('task_text')}
            )
        
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Task service unavailable'}), 503

@app.route('/tasks/<user_id>', methods=['GET'])
@token_required
def get_tasks(user_id):
    try:
        response = requests.get(
            f"{app.config['TASK_SERVICE_URL']}/tasks/{user_id}"
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Task service unavailable'}), 503

@app.route('/tasks/complete/<task_id>', methods=['PUT'])
@token_required
def complete_task(task_id):
    try:
        response = requests.put(
            f"{app.config['TASK_SERVICE_URL']}/tasks/complete/{task_id}"
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Task service unavailable'}), 503

@app.route('/tasks/history/<user_id>', methods=['GET'])
@token_required
def get_task_history(user_id):
    try:
        response = requests.get(
            f"{app.config['TASK_SERVICE_URL']}/tasks/history/{user_id}"
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Task service unavailable'}), 503

@app.route('/tasks/<task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    try:
        response = requests.put(
            f"{app.config['TASK_SERVICE_URL']}/tasks/{task_id}", 
            json=request.get_json()
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Task service unavailable'}), 503

# Suggestion routes
@app.route('/suggestions', methods=['GET'])
@token_required
def get_suggestions():
    try:
        response = requests.get(
            f"{app.config['SUGGESTION_SERVICE_URL']}/suggestions",
            params={'q': request.args.get('q', '')}
        )
        return handle_service_error(response)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Suggestion service unavailable'}), 503 