from App import app
from flask import jsonify
from datetime import datetime

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "status": "ok",
        "date": datetime.utcnow().isoformat()
    }), 200

users = {
    1: {"id": 1, "name": "Bohdan"},
    2: {"id": 2, "name": "Vlad"},
    3: {"id": 3, "name": "Sasha"}
}

# Користувачі
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user_id = len(users) + 1
    users[user_id] = {"id": user_id, "name": data["name"]}
    return jsonify(users[user_id]), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(users.get(user_id)) if user_id in users else ("Not found", 404)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    return "Not found", 404