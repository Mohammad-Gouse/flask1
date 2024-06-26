import csv
import http
import os

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var

TRANSACTION_FILE_NAME = Data_Var.data_store_location


def upload_client_master(data):
    from app import db
    from src.models.nominee_client_master import nominee_client_master_model

    try:
        # csv_fields = data[0].split(",")
        csv_reader=csv.reader(data)
        header=next(csv_reader)
        fields_of_db_table = Data_Var.nominee_client_master_header.split(",")
        # print(set(csv_fields) != set(fields_of_db_table))
        # print("csv fileds", csv_fields, len(csv_fields))
        # print("fields of db", fields_of_db_table, len(fields_of_db_table))
        if set(header) != set(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload valid file."}), 400)

        # data.pop(0)
        bulk_insert_data = []
        count = 0
        for row in csv_reader:
            single_record = nominee_client_master_model(row)
            # if single_record.client_id != '':
            query_to_check_record_exist = db.session.query(nominee_client_master_model.id).filter(
                nominee_client_master_model.client_id == single_record.client_id
            )
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            db.session.add(single_record)
            count += 1
        db.session.commit()
        return make_response(
            {"message": str(count) + " records added successfully"}
        )
    except sqlalchemy.exc.DatabaseError as e:
        print(e)
        db.session.rollback()
        return make_response("Please check database connection")
