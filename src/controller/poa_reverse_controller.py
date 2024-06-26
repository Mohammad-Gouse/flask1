import http
import csv
# from dbfread.field_parser import FieldParser
import dbf
# import dbfread
import zipfile
import time
from dbf import Table
import os
# from dbfread import DBF
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file, Response
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var

fields = ['REGCODE', 'CLIENTID', 'CLIENTNAME', 'BROKERCODE', 'AMCCODE', 'SCHEMECODE', 'SECURITYNAME',
          'FOLIONO', 'TRANTYPE', 'ORDERDATE', 'QTY', 'AMOUNT', 'STATUS', 'REMARKS', 'ORDERID', 'USERTRXNNO', 'POA']
TRANSACTION_FILE_NAME = Data_Var.data_store_location


def upload_poa(data):
    from app import db
    from src.models.nominee_client_master import nominee_client_master_model
    from src.models.poa_model import poa_model

    try:
        csv_fields = data[0].split(",")
        fields_of_db_table = Data_Var.poa_headers.split(",")
        # print("fields of db t: ", fields_of_db_table)
        # print("fields of csv_fiels ", csv_fields)
        if set(csv_fields) != set(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload a valid file."}), 401)

        # query_to_check_records_exist_in_client_master = db.session.query(
        #     nominee_client_master_model).first()
        # if query_to_check_records_exist_in_client_master is None:
        #     return make_response(jsonify({"message": "Please upload client master file first."}), 402)

        data.pop(0)
        count = 0
        matching_records = []
        for row in data:
            single_record = poa_model(row.split(","))
            query_to_check_record_exist = db.session.query(poa_model.id).filter(
                poa_model.usertrxnno == single_record.usertrxnno)
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            # query_to_check_record_in_client_master = db.session.query(nominee_client_master_model).filter(
            #     nominee_client_master_model.client_id == single_record.clientid).first()
            # if (query_to_check_record_in_client_master):
                # print("Matching record in client master:", row)
            matching_records.append(row)
            db.session.add(single_record)
            count += 1
        db.session.commit()

        if matching_records:
            csv_file_path, csv_file_name = save_matching_records_to_csv(
                matching_records)
            dbf_file_path, dbf_file_name = csv_to_dbf(
                csv_file_path, csv_file_name)
            zip_folder_name = f'{csv_file_name}'

            zip_folder = f'{TRANSACTION_FILE_NAME}/nominee/poa/{zip_folder_name}'
            os.mkdir(zip_folder)

            # Add the CSV and DBF files to the zip archive
            dbt_new_path = os.path.join(zip_folder, f"{csv_file_name}.dbt")
            dbf_file_path = os.path.join(zip_folder, f"{dbf_file_name}")

            os.rename(
                f'{TRANSACTION_FILE_NAME}/nominee/poa/{csv_file_name}.dbt', dbt_new_path)
            os.rename(
                f'{TRANSACTION_FILE_NAME}/nominee/poa/{dbf_file_name}', dbf_file_path)
            zip_file_name = f'{TRANSACTION_FILE_NAME}/nominee/poa/{csv_file_name}.zip'

            # with zipfile.ZipFile(zip_file_name, "w") as zipf:
            #     zipf.write(dbt_new_path, arcname=f'{zip_folder_name}/{csv_file_name}.dbt')
            #     zipf.write(dbf_file_path, arcname=f'{zip_folder_name}/{dbf_file_name}')
            with zipfile.ZipFile(zip_file_name, "w") as zipf:
                # Add the CSV and DBF files to the zip archive
                for root, _, files in os.walk(zip_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, zip_folder)
                        zipf.write(file_path, arcname=arcname)

            return zip_file_name, csv_file_name
        else:
            # return "No matching records found."
            return make_response(jsonify({"message": "Please update the file with new records"}),
                                 400)

        #    return  str(count) + " records added successfully"
    except sqlalchemy.exc.DatabaseError as e:
        # print(e)
        db.session.rollback()
        return make_response("Please check the database connection", 500)


# zip_folder_counter = 1


def save_matching_records_to_csv(records):
    # global zip_folder_counter
    csv_file_name = generate_file_name_with_epoch()
    zip_file_path = f'{TRANSACTION_FILE_NAME}/nominee/poa'
    os.makedirs(zip_file_path, exist_ok=True)
    csv_file_path = f'{TRANSACTION_FILE_NAME}/nominee/poa/{csv_file_name}.csv'
    # zip_folder_counter = zip_folder_counter+1
    # print(zip_folder_counter)
    with open(csv_file_path, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(fields)
        for record in records:
            csv_writer.writerow(record.split(','))

    return csv_file_path, csv_file_name


def csv_to_dbf(csv_file_path, csv_file_name):
    dbf_file_name = f'{csv_file_name}.dbf'
    dbf_file_path = os.path.join(
        f'{TRANSACTION_FILE_NAME}/nominee/poa/', dbf_file_name)
    # dbf_file_path = os.path.join(
    #     f'{TRANSACTION_FILE_NAME}/nominee/poa/{csv_file_name}', dbf_file_name)
    # folder_path = os.path.join(f'{TRANSACTION_FILE_NAME}/nominee/poa/', f'{csv_file_name}')
    # os.makedirs(folder_path, exist_ok=True)
    tables = dbf.from_csv(csvfile=f'{csv_file_path}', filename=dbf_file_path,
                          field_names='REGCODE CLIENTID CLIENTNAME BROKERCODE AMCCODE SCHEMECODE SECURINAME FOLIONO TRANTYPE ORDERDATE QTY AMOUNT STATUS REMARKS ORDERID USERTRXNNO POA'.split())

    return dbf_file_path, dbf_file_name


def generate_file_name_with_epoch():

    current_time = int(time.time())  # Get current epoch time

    # Create a file name using epoch time
    file_name = f"POA_MATCHING_FILE_{current_time}"

    return file_name
