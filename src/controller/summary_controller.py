import csv
import datetime
import http
import os

import pandas.errors
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var
from src.utils.oracledb import session_pool
from src.utils.psqldb import get_connection_from_pool, psql_connect

TRANSACTION_FILE_NAME = Data_Var.data_store_location


# def get_poa_summary(data):
#     import pandas as pd
#     file_name = data.get('filename')
#     sub_folder_name = "poa_summary"
#     try:
#         pool = psql_connect()
#         if not pool:
#             return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

#         ps_connection = get_connection_from_pool(pool)
#         if ps_connection:
#             ps_cursor = ps_connection.cursor()
#             start_date = data.get('start_date')
#             end_date = data.get('end_date')
#             if start_date == end_date:
#                 date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
#                 date = date + datetime.timedelta(days=1)
#                 end_date = date.strftime("%m-%d-%Y")
#             else:
#                 end_date = datetime.datetime.strptime(
#                     end_date, '%d-%m-%Y').date().strftime("%m-%d-%Y")
#             start_date = datetime.datetime.strptime(
#                 start_date, '%d-%m-%Y').date().strftime("%m-%d-%Y")
#             output_query = f"COPY ({Data_Var.poa_download_summary}) TO STDOUT WITH (FORMAT CSV, DELIMITER ',', HEADER);".format(
#                 start_date, end_date)
#             isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
#             if not isExist:
#                 # Create a new directory because it does not exist
#                 os.makedirs(f'{TRANSACTION_FILE_NAME}')
#             # check if transaction directory exist
#             isTransactionDirExist = os.path.exists(
#                 f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
#             if not isTransactionDirExist:
#                 # Create a new directory because it does not exist
#                 os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

#             with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
#                 # creating csv file using query
#                 ps_cursor.copy_expert(output_query, f)
#                 f.close()
#             ps_cursor.close()
#             if len(pd.read_csv(
#                     f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')) < 1:
#                 os.remove(
#                     f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
#                 return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
#             return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}',
#                              as_attachment=True)

#     except psycopg2.DatabaseError as error:
#         print(error)
#         os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
#         return make_response(jsonify({"message": "Please check database connection details"}),
#                              http.HTTPStatus.INTERNAL_SERVER_ERROR)

def get_poa_summary(data):
    import pandas as pd
    file_name = data.get('filename')
    sub_folder_name = "poa_summary"
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            if start_date == end_date:
                date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
                date = date + datetime.timedelta(days=1)
                end_date = date.strftime("%m-%d-%Y")
            else:
                end_date = datetime.datetime.strptime(
                    end_date, '%d-%m-%Y').date().strftime("%m-%d-%Y")
            start_date = datetime.datetime.strptime(
                start_date, '%d-%m-%Y').date().strftime("%m-%d-%Y")
            output_query = f"COPY ({Data_Var.poa_download_summary}) TO STDOUT WITH (FORMAT CSV, DELIMITER ',', HEADER);".format(
                start_date, end_date)
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(
                f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            if len(pd.read_csv(
                    f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')) < 1:
                os.remove(
                    f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}',
                             as_attachment=True)

    except psycopg2.DatabaseError as error:
        print(error)
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def get_rta_summary(data):
    import pandas as pd
    file_name = data.get('filename')
    sub_folder_name = "rta_summary"
    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            print("start data: ", start_date)
            print("end data: ", end_date)
            if start_date == end_date:
                date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
                date = date + datetime.timedelta(days=1)
                end_date = date.strftime("%m-%d-%Y")
            else:
                end_date = datetime.datetime.strptime(
                    end_date, '%d-%m-%Y').date().strftime("%Y-%m-%d")
            start_date = datetime.datetime.strptime(
                start_date, '%d-%m-%Y').date().strftime("%Y-%m-%d")
            output_query = f"COPY ({Data_Var.rta_download_summary}) TO STDOUT WITH (FORMAT CSV, DELIMITER ',', HEADER);".format(
                start_date, end_date)
            print("start data: ", start_date)
            print("end data: ", end_date)
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            isTransactionDirExist = os.path.exists(
                f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')
            if not isTransactionDirExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)

                print("ps_cursor: ", ps_cursor)
                print("output query: ", output_query)
                f.close()
            ps_cursor.close()
            if len(pd.read_csv(
                    f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')) < 1:
                os.remove(
                    f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)
            return send_file(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}',
                             as_attachment=True)

    except psycopg2.DatabaseError as error:
        print(error)
        os.remove(f'{TRANSACTION_FILE_NAME}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)
