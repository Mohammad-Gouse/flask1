import csv
import http
import os

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify, request
import jwt

from src.utils.data_variable import Data_Var

TRANSACTION_FILE_NAME = Data_Var.data_store_location


def upload_poa(data):
    from app import db
    from src.models.poa_model import poa_model

    try:
        # csv_fields = data[0].split(",")
        csv_reader = csv.reader(data)
        header = next(csv_reader)
        fields_of_db_table = Data_Var.poa_headers.split(",")
        # print(set(csv_fields) != set(fields_of_db_table))
        # print("csv fileds", csv_fields, len(csv_fields))
        # print("fields of db", fields_of_db_table, len(fields_of_db_table))
        if set(header) != set(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload valid file."}), 400)

        # data.pop(0)
        bulk_insert_data = []
        count = 0
        for row in csv_reader:
            single_record = poa_model(row)
            # if single_record.client_id != '':
            query_to_check_record_exist = db.session.query(poa_model.id).filter(
                poa_model.usertrxnno == single_record.usertrxnno
            )
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            db.session.add(single_record)
            count += 1

        token = request.headers.get("Authorization")
        if not token:
            return make_response(jsonify({"message": "Unauthorized"}), http.HTTPStatus.UNAUTHORIZED)

        # Extract the user_name from the token
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            user_name = payload.get("user_name")
            print("user_name:", user_name)
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token expired"}), http.HTTPStatus.UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return make_response(jsonify({"message": "Invalid token"}), http.HTTPStatus.UNAUTHORIZED)

        db.session.commit()
        return make_response(
            {"message": str(count) + " records added successfully"}
        )
    except sqlalchemy.exc.DatabaseError as e:
        print(e)
        db.session.rollback()
        return make_response("Please check database connection")
