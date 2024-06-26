import http
import os
import csv
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var


TRANSACTION_FILE_NAME = Data_Var.data_store_location


def upload_karvy_feed(data):
    from app import db
    from src.models.nominee_karvy_reverse_feed import nominee_karvy_reverse_field

    try:
        # csv_fields = data[0].split(",")
        csv_reader=csv.reader(data)
        header=next(csv_reader)
        fields_of_db_table = Data_Var.nominee_karvy_reverse_header.split(",")
        if set(header) != set(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload a valid file."}), 400)

        count = 0
        for row in csv_reader:
            single_record = nominee_karvy_reverse_field(row)
            query_to_check_record_exist = db.session.query(nominee_karvy_reverse_field.id).filter(
                nominee_karvy_reverse_field.ih_no == single_record.ih_no)
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            db.session.add(single_record)
            count += 1
        db.session.commit()
        return make_response({"message": str(count) + " records added successfully"}, 200)
    except sqlalchemy.exc.DatabaseError as e:
        print(e)
        db.session.rollback()
        return make_response("Please check the database connection", 500)
