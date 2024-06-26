from flask import Flask, jsonify
import pandas as pd
import csv
import datetime
import http
import os
import zipfile

import psycopg2
from flask import send_file
from flask import make_response, jsonify

from src.utils.data_variable import Data_Var
from src.utils.psqldb import get_connection_from_pool, psql_connect

TRANSACTION_FILE_NAME = Data_Var.data_store_location


def get_file_name(main, sub_folder):
    main_folder_name = main
    sub_folder_name = sub_folder
    # Get the current date in the format "DDMMYYYY"
    current_date = datetime.datetime.now().strftime("%d%m%Y")
    is_exist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(f'{TRANSACTION_FILE_NAME}')
    is_main_folder_exist = os.path.exists(
        f'{TRANSACTION_FILE_NAME}/{main_folder_name}')
    if not is_main_folder_exist:
        # Create a new directory because it does not exist
        os.makedirs(f'{TRANSACTION_FILE_NAME}/{main_folder_name}')
    is_sub_older_Exist = os.path.exists(
        f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')
    if not is_sub_older_Exist:
        # Create a new directory because it does not exist
        os.makedirs(
            f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')

    # Get the list of files in the target directory with the format "CAMNOMDDMMYYYY_1" and extract the suffixes
    files_in_directory = os.listdir(
        f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')
    # suffixes = [int(file_name.split('_')[-1])
    #             for file_name in files_in_directory if file_name.startswith(f"AOFCAMS{current_date}_")]
    suffixes = [
        # Extract the numeric part before the extension
        int(file_name.split('_')[-1].split('.')[0])
        for file_name in files_in_directory
        if file_name.startswith(f"AOFCAMS{current_date}_")
    ]

    # Increment the filename suffix by finding the maximum value and adding 1
    if suffixes:
        next_suffix = max(suffixes) + 1
    else:
        next_suffix = 1

    # Create the new filename with the incremented suffix
    file_name = f"AOFCAMS{current_date}_{next_suffix}"
    return f'{file_name}.txt'


QUERY = """
    SELECT 'IIFLWPMS' AS iiflw_pms, cm.pan_number, rta.client_name, 'AOF' AS iiflw_pms,
    CONCAT('IIFLWPMS$',cm.pan_number,'$AOF') AS file_name
    FROM rta_reverse_feed_details rta
    INNER JOIN client_master cm ON cm.client_id = rta.client_id
    WHERE rta.trant_type = 'P' AND (rta.folio_no IS NULL OR rta.folio_no = 0)
"""


def get_month_name(month_number):
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY",
                   "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return month_names[month_number - 1]


def get_aof_cams(file_name):
    folder_year = datetime.datetime.now().strftime("%Y")
    folder_month = get_month_name(int(datetime.datetime.now().strftime("%m")))
    folder_day = datetime.datetime.now().strftime("%d")
    main_folder_name = "aof"
    sub_folder_name = f'cams/{folder_year}/{folder_month}/{folder_day}'
    file_name = get_file_name(main_folder_name, sub_folder_name)

    try:
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            output_query = f"COPY ({QUERY}) TO STDOUT WITH (FORMAT TEXT, DELIMITER '{Data_Var.file_delimiter}');"
            isExist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}')
            # check if transaction directory exist
            is_main_folder_exist = os.path.exists(
                f'{TRANSACTION_FILE_NAME}/{main_folder_name}')
            if not is_main_folder_exist:
                # Create a new directory because it does not exist
                os.makedirs(f'{TRANSACTION_FILE_NAME}/{main_folder_name}')
            is_sub_folder_exist = os.path.exists(
                f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')
            if not is_sub_folder_exist:
                # Create a new directory because it does not exist
                os.makedirs(
                    f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')

            with open(f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{file_name}', 'w') as f:
                # creating csv file using query
                ps_cursor.copy_expert(output_query, f)
                f.close()
            ps_cursor.close()
            db_response = pd.read_csv(
                f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{file_name}')
            if len(db_response) < 1:
                os.remove(
                    f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{file_name}')
                return make_response(jsonify({"message": "No new transaction found"}), http.HTTPStatus.NOT_FOUND)

            folder_path = f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}'

            return download_folder(folder_path, f'{folder_day}.zip')

    except psycopg2.DatabaseError as error:
        print(error)
        os.remove(
            f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def download_folder(folder_path, zip_filename):
    # folder_path = '/path/to/your/folder'  # Replace this with the path to your folder
    # zip_filename = 'downloaded_folder.zip'

    # Create a temporary zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Send the zip file as an attachment for download
    return send_file(zip_filename, as_attachment=True)
