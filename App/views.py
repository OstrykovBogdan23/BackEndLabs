from App import app
from flask import Flask
from flask import jsonify
from flask import request
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

categories = {
    1: {"id": 1, "name": "Food"},
    2: {"id": 2, "name": "Clothes"},
    3: {"id": 3, "name": "Entertainment"}
}

records = {
    1: {"id": 1, "user_id": 1, "category_id": 1, "amount": 120, "date": "2025-01-27T12:00:00"},
    2: {"id": 2, "user_id": 2, "category_id": 2, "amount": 800, "date": "2025-01-28T09:30:00"},
    3: {"id": 3, "user_id": 1, "category_id": 2, "amount": 699, "date": "2025-01-28T09:40:00"},
    4: {"id": 4, "user_id": 2, "category_id": 3, "amount": 200, "date": "2025-01-28T09:30:00"}
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



# Категорії
@app.route('/category', methods=['POST'])
def create_category():
    data = request.json
    category_id = len(users) + 1
    categories[category_id] = {"id": category_id, "name": data["name"]}
    return jsonify(categories[category_id]), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values()))

@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return jsonify(categories.get(category_id)) if category_id in categories else ("Not found", 404)

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in categories:
        del categories[category_id]
        return '', 204
    return "Not found", 404



# Записи витрат
@app.route('/record', methods=['POST'])
def create_record():
    data = request.json
    record_id = len(records)+1
    records[record_id] = {
        "id": record_id,
        "user_id": data["user_id"],
        "category_id": data["category_id"],
        "amount": data["amount"],
        "date": datetime.utcnow().isoformat()
    }
    return jsonify(records[record_id]), 201

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    return jsonify(records.get(record_id)) if record_id in records else ("Not found", 404)

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return '', 204
    return "Not found", 404

@app.route('/record', methods=['GET'])
def get_filtered_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return "User ID або Category ID обов'язкові", 400

    filtered = list(records.values())
    if user_id is not None:
        filtered = [r for r in filtered if r["user_id"] == user_id]
    if category_id is not None:
        filtered = [r for r in filtered if r["category_id"] == category_id]

    return jsonify(filtered)