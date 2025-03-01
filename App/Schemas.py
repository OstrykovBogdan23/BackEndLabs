from app import ma
from app.models import User, Income, Category, Record

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class IncomeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Income
        load_instance = True

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

class RecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Record
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
income_schema = IncomeSchema()
incomes_schema = IncomeSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
record_schema = RecordSchema()
records_schema = RecordSchema(many=True)
