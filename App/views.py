from app import app, db
from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime
from models import User, Income, Category, Record

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
    return jsonify({"id": new_user.id, "name": new_user.name, "balance": new_user.balance}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ "id": user.id, "name": user.name, "balance": user.balance } for user in users])

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Користувач не знайдений"}), 404
    return jsonify({"id": user.id, "name": user.name, "balance": user.balance})

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
    return jsonify({"id": new_income.id, "user_id": new_income.user_id, "amount": new_income.amount}), 201

@app.route('/income/<int:income_id>', methods=['GET'])
def get_income(income_id):
    income = Income.query.get(income_id)
    if not income:
        return jsonify({"error": "Запис не знайдено"}), 404
    return jsonify({"id": income.id, "user_id": income.user_id, "amount": income.amount})

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
    return jsonify({"id": new_record.id, "user_id": new_record.user_id, "category": new_record.category,
                    "amount": new_record.amount}), 201

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.get(record_id)
    if not record:
        return jsonify({"error": "Запис не знайдено"}), 404
    return jsonify({"id": record.id, "user_id": record.user_id, "category": record.category, "amount": record.amount})

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
    records_list = [{"id": r.id, "user_id": r.user_id, "category": r.category, "amount": r.amount, "date": r.date.isoformat()} for r in records]

    return jsonify(records_list)

# Категорії
@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data["name"])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"id": new_category.id, "name": new_category.name}), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{ "id": category.id, "name": category.name} for category in categories])

@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Категорію не знайдено"}), 404
    return jsonify({"id": category.id, "name": category.name})

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Категорію не знайдено"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Категорію видалено"}), 200