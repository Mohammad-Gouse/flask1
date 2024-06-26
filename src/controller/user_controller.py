import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from flask import make_response, jsonify
from decouple import config


DB_TABLE_UTILITY = config('DB_TABLE_UTILITY')
TRANSACTION_FILE_NAME = config('TRANSACTION_FILE_NAME')


def add_users(data):
    try:
        from src.models.users_model import Users
        import app
        users_object = Users(data.get('username'), data.get('password'))
        app.db.session.add(users_object)
        app.db.session.commit()
        return {'message': 'User is added successfully'}
    except sqlalchemy.exc.DatabaseError as err:
        return err.orig.pgerror


def get_users():
    try:
        from src.models.users_model import Users
        import app
        response = app.db.session.query(Users).all()
        return jsonify([item.to_dict() for item in response])
    except SQLAlchemyError as error:
        return make_response(jsonify("message", error), 400)


def update_users(data):
    try:
        from src.models.users_model import Users
        import app
        app.db.session.query(Users).filter(Users.user_name == data.get('username')).update(
            {"password": data.get('password')}, synchronize_session="fetch"
        )
        app.db.session.commit()
        return {"message": "User is updated"}
    except sqlalchemy.exc.DatabaseError:
        return
