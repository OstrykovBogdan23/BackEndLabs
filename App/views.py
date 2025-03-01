from app import app
from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime
from app.models import *
from app.schemas import *

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "App is running"})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "status": "ok",
        "date": datetime.utcnow().isoformat()
    }), 200

# Користувачі
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data["name"])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Користувач не знайдений"}), 404
    return user_schema.jsonify(user)

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Користувач не знайдений"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Користувач видалений"}), 200

# Надходження
@app.route('/income', methods=['POST'])
def create_income():
    data = request.get_json()
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "Користувач не знайдений"}), 404
    new_income = Income(user_id=data["user_id"], amount=data["amount"])
    db.session.add(new_income)
    user.balance += data["amount"]
    db.session.commit()
    return income_schema.jsonify(new_income), 201

@app.route('/income/<int:income_id>', methods=['GET'])
def get_income(income_id):
    income = Income.query.get(income_id)
    if not income:
        return jsonify({"error": "Запис не знайдено"}), 404
    return income_schema.jsonify(income)

@app.route('/income/<int:income_id>', methods=['DELETE'])
def delete_income(income_id):
    income = Income.query.get(income_id)
    if not income:
        return jsonify({"error": "Запис не знайдено"}), 404
    db.session.delete(income)
    db.session.commit()
    return jsonify({"message": "Запис видалено"}), 200



# Записи витрати
@app.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "Користувач не знайдений"}), 404
    if user.balance < data["amount"]:
        return jsonify({"error": "Недостатньо коштів"}), 400
    new_record = Record(user_id=data["user_id"], category=data["category"], amount=data["amount"])
    db.session.add(new_record)
    user.balance -= data["amount"]
    db.session.commit()
    return record_schema.jsonify(new_record), 201

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.get(record_id)
    if not record:
        return jsonify({"error": "Запис не знайдено"}), 404
    return record_schema.jsonify(record)

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = Record.query.get(record_id)
    if not record:
        return jsonify({"error": "Запис не знайдено"}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Запис видалено"}), 200

@app.route('/records', methods=['GET'])
def get_filtered_records():
    user_id = request.args.get("user_id", type=int)
    category = request.args.get("category", type=str)

    query = Record.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category:
        query = query.filter_by(category=category)

    records = query.all()
    return records_schema.jsonify(records)

# Категорії
@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data["name"])
    db.session.add(new_category)
    db.session.commit()
    return category_schema.jsonify(new_category), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return categories_schema.jsonify(categories)

@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Категорію не знайдено"}), 404
    return category_schema.jsonify(category)

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Категорію не знайдено"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Категорію видалено"}), 200
