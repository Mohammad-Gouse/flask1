# import http
# import os
# import csv
# import dbf
# import zipfile
# import sqlalchemy
# from sqlalchemy.exc import SQLAlchemyError
# import psycopg2
# from flask import send_file, make_response, jsonify
# import time
# from datetime import datetime
# from src.utils.data_variable import Data_Var

# fields = ['REGCODE', 'CLIENTID', 'CLIENTNAME', 'BROKERCODE', 'AMCCODE', 'SCHEMECODE', 'SECURITYNAME',
#           'FOLIONO', 'TRANTYPE', 'ORDERDATE', 'QTY', 'AMOUNT', 'STATUS', 'REMARKS', 'ORDERID', 'USERTRXNNO']

# TRANSACTION_FILE_NAME = Data_Var.data_store_location


# def upload_rta_reverse_feed(data):
#     from app import db
#     from src.models.nominee_rta_reverse import nominee_rta_reverse_model
#     from src.models.nominee_client_master import nominee_client_master_model
#     from src.models.nominee_karvy_reverse_feed import nominee_karvy_reverse_field

#     try:
#         # csv_fields = data[0].split(",")
#         csv_reader = csv.reader(data)
#         header = next(csv_reader)
#         fields_of_db_table = Data_Var.nominee_rta_reverse_headers.split(",")

#         if set(header) != set(fields_of_db_table):
#             return make_response(jsonify({"message": "Please upload valid file."}), 401)

#         query_to_check_records_exist_in_client_master = db.session.query(
#             nominee_client_master_model)

#         if query_to_check_records_exist_in_client_master is None:
#             return make_response(jsonify({"message": "Please upload client master file first."}), 402)

#         # data.pop(0)
#         count = 0
#         matching_records = []
#         matching_records_karvy = []
#         matching_records_cam_nom = []
#         karvy_count = 0
#         cams_count = 0
#         sr_no = 1
#         field = ""
#         field1 = "1"
#         field2 = "N"
#         field3 = "OF"
#         field4 = "AOF/POA/BR/ASL/PAN/KYC"
#         field5 = "Y"
#         for row in csv_reader:
#             single_record = nominee_rta_reverse_model(row)

#             query_to_check_record_exist = db.session.query(nominee_rta_reverse_model.id).filter(
#                 nominee_rta_reverse_model.user_trxn_no == single_record.user_trxn_no
#             )
#             query_to_check_record_in_client_master = db.session.query(nominee_client_master_model.id).filter(
#                 nominee_client_master_model.client_id == single_record.client_id).first()

#             print("client match: ", query_to_check_record_in_client_master)

#             if db.session.query(query_to_check_record_exist.exists()).scalar():
#                 continue
#             if query_to_check_record_in_client_master is not None:
#                 if single_record.reg_code.lower() == "cams":
#                     cams_count = cams_count + 1
#                     pan_number_tuple = db.session.query(nominee_client_master_model.pan_number).filter(
#                         nominee_client_master_model.client_id == single_record.client_id).first()
#                     pan_number = pan_number_tuple[0]
#                     print("REG CODE:", single_record.reg_code)
#                     matching_records.append((single_record.client_id, single_record.client_name, pan_number))
#                     matching_records_cam_nom.append(
#                         (single_record.amc_code, single_record.user_trxn_no, pan_number, single_record.client_name))
#                 elif single_record.reg_code.lower() == "karvy":
#                     karvy_count = karvy_count + 1
#                     pan_number_tuple = db.session.query(nominee_client_master_model.pan_number).filter(
#                         nominee_client_master_model.client_id == single_record.client_id).first()
#                     pan_number = pan_number_tuple[0]
#                     print("pan_number",pan_number)
#                     ih_no = db.session.query(nominee_karvy_reverse_field.ih_no).filter(
#                         nominee_karvy_reverse_field.usr_txn_no == single_record.user_trxn_no
#                     ).scalar()
#                     print("IH_NO: ", ih_no)
#                     print("REG CODE:", single_record.reg_code)
#                     matching_records_karvy.append((
#                         sr_no, single_record.user_trxn_no, pan_number, single_record.amc_code,
#                         single_record.broker_code, single_record.broker_code, field, field,
#                         single_record.client_name, field1, field2, field3, field4, pan_number,
#                         ih_no, field5))
#                     sr_no += 1
#             if query_to_check_record_in_client_master is not None:
#                 db.session.add(single_record)

#             count += 1

#         db.session.commit()

#         if matching_records or matching_records_karvy or matching_records_cam_nom:
#             csv_file_path, csv_file_name = save_matching_records_to_csv(
#                 matching_records_karvy)
#             dbf_file_path, dbf_file_name, dbf_file_name_without = csv_to_dbf(
#                 csv_file_path, csv_file_name)
#             csv_file_path, csv_file_name = save_matching_records_to_csv(matching_records)
#             txt_file_path, txt_file_name = csv_to_txt(csv_file_path, csv_file_name, matching_records)
#             csv_file_path, csv_file_name = save_matching_records_to_csv(matching_records_cam_nom)
#             txt_file_path_nom, txt_file_name_nom = csv_to_txt_nom(csv_file_path, csv_file_name, matching_records_cam_nom)
#             time = generate_file_name_with_epoch()
#             zip_folder_name = f'CAMS_NOM_{time}'
#             zip_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/{zip_folder_name}'
#             os.mkdir(zip_folder)
#             dbt_new_path = os.path.join(zip_folder, f"{dbf_file_name_without}.dbt")
#             dbf_file_path = os.path.join(zip_folder, f"{dbf_file_name}")
#             txt_file_paths = os.path.join(zip_folder, f"{txt_file_name}.txt")
#             txt_file_paths_nom=os.path.join(zip_folder,f"{txt_file_name_nom}.txt")
#             os.rename(
#                 f'{TRANSACTION_FILE_NAME}/nominee/cams/{dbf_file_name_without}.dbt', dbt_new_path)
#             os.rename(
#                 f'{TRANSACTION_FILE_NAME}/nominee/cams/{dbf_file_name}', dbf_file_path)
#             os.rename(f'{TRANSACTION_FILE_NAME}/nominee/cams/{txt_file_name}.txt', txt_file_paths)
#             os.rename(f'{TRANSACTION_FILE_NAME}/nominee/cams/{txt_file_name_nom}.txt', txt_file_paths_nom)

#             zip_file_name = f'{TRANSACTION_FILE_NAME}/nominee/cams/{zip_folder_name}.zip'

#             with zipfile.ZipFile(zip_file_name, "w") as zipf:
#                 for root, _, files in os.walk(zip_folder):
#                     for file in files:
#                         file_path = os.path.join(root, file)
#                         arcname = os.path.relpath(file_path, zip_folder)
#                         zipf.write(file_path, arcname=arcname)

#             return zip_file_name, zip_folder_name
#         else:
#             return make_response(jsonify({"message": "Please update the file with new records"}), 400)

#     except sqlalchemy.exc.DatabaseError as e:
#         db.session.rollback()
#         return make_response("Please check database connection")


# def save_matching_records_to_csv(records):
#     csv_file_name = generate_file_name_with_epoch()
#     zip_file_path = f'{TRANSACTION_FILE_NAME}/nominee/cams'
#     os.makedirs(zip_file_path, exist_ok=True)
#     csv_file_path = f'{TRANSACTION_FILE_NAME}/nominee/cams/{csv_file_name}.csv'
#     with open(csv_file_path, 'w', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         for record in records:
#             csv_writer.writerow(record)
#         return csv_file_path, csv_file_name


# def csv_to_dbf(csv_file_path, csv_file_name):
#     formatted_date = current_date.strftime("%y%m%d")
#     time = generate_file_name_with_epoch()
#     dbf_file_name_without = f'DOC_5874{formatted_date}_{time}'
#     dbf_file_name = f'{dbf_file_name_without}.dbf'
#     dbf_file_path = os.path.join(
#         f'{TRANSACTION_FILE_NAME}/nominee/cams/', dbf_file_name)
#     tables = dbf.from_csv(csvfile=f'{csv_file_path}', filename=dbf_file_path,
#                           field_names='FIELD1 FIELD2 FIELD3 FIELD4 FIELD5 FIELD6 FIELD7 FIELD8 FIELD9 FIELD10 FIELD11 FIELD12 FIELD13 FIELD14 FIELD15 FIELD16'.split())
#     return dbf_file_path, dbf_file_name, dbf_file_name_without


# def csv_to_txt(csv_file_path, csv_file_name, data):
#     time = generate_file_name_with_epoch()
#     txt_file_name = f'CAMS_AOF_{time}'
#     txt_file_path = f'{TRANSACTION_FILE_NAME}/nominee/cams/{txt_file_name}.txt'

#     static_field1 = "IFFWPMS"
#     static_field3 = "AOF"

#     with open(txt_file_path, 'w') as txt_file:
#         for row in data:
#             fields = row

#             # Assuming the order of fields in the CSV matches your requirements,
#             # you can fetch values from specific columns (adjust indices accordingly)
#             # client_id = fields[0]  # Index for CLIENTID

#             client_name = fields[1]  # Index for CLIENTNAME

#             pan_number = fields[2]
#             # Construct the dynamic part of the line
#             # dynamic_part = f"{pan_number}|{client_name}|{static_field3}"

#             # Combine static and dynamic parts to create the line
#             line = f"{static_field1}|{pan_number}|{client_name}|{static_field3}|{static_field1}${pan_number}${static_field3}"

#             txt_file.write(line + '\n')

#     return txt_file_path, txt_file_name


# def csv_to_txt_nom(csv_file_path, csv_file_name, data):
#     time = generate_file_name_with_epoch()
#     txt_file_name = f'CAMS_NOM_{time}'
#     txt_file_path = f'{TRANSACTION_FILE_NAME}/nominee/cams/{txt_file_name}.txt'

#     static_field1 = "IFFWPMS"
#     static_field3 = "NOM"
#     empty=""
#     fn="FN"

#     with open(txt_file_path, 'w') as txt_file:
#         for row in data:
#             fields = row

#             # Assuming the order of fields in the CSV matches your requirements,
#             # you can fetch values from specific columns (adjust indices accordingly)
#             # client_id = fields[0]  # Index for CLIENTID

#             amc_code=fields[0]
#             user_no=fields[1]
#             pan_no=fields[2]
#             client_name=fields[3]

#             # Construct the dynamic part of the line
#             # dynamic_part = f"{pan_number}|{client_name}|{static_field3}"

#             # Combine static and dynamic parts to create the line
#             line = f"{amc_code}|{static_field1}|{user_no}|{pan_no}|{client_name}|{fn}${amc_code}${static_field1}${user_no}|{empty}|{static_field3}"

#             txt_file.write(line + '\n')

#     return txt_file_path, txt_file_name


# def generate_file_name_with_epoch():
#     current_time = int(time.time())
#     # file_name = f"RTA_MATCHING_FILE_{current_time}"

#     return current_time


# current_date = datetime.now()

# # Format the date as YYMMDD

import http
import os

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var


TRANSACTION_FILE_NAME = Data_Var.data_store_location


def upload_rta_reverse_feed(data, user):
    from app import db
    from src.models.nominee_rta_reverse import nominee_rta_reverse_model
    from src.models.users_model import Users

    try:
        csv_fields = data[0].split(",")
        fields_of_db_table = Data_Var.nominee_rta_reverse_headers.split(",")
        # print(set(csv_fields) != set(fields_of_db_table))
        # print(csv_fields)
        # print(fields_of_db_table)
        if set(csv_fields) != set(fields_of_db_table):
            return make_response(jsonify({"message": "Please upload valid file."}), 400)
        data.pop(0)
        # bulk_insert_data = []
        count = 0
        for row in data:
            single_record = nominee_rta_reverse_model(row.split(","))
            # if single_record.user_trxn_no != '':
            query_to_check_record_exist = db.session.query(nominee_rta_reverse_model.id).filter(
                nominee_rta_reverse_model.user_trxn_no == single_record.user_trxn_no
            )
            if db.session.query(query_to_check_record_exist.exists()).scalar():
                continue
            userid = db.session.query(Users.id).filter(
                Users.user_name == user
            ).first()
            single_record.created_by = userid[0]
            single_record.updated_by = userid[0]
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
