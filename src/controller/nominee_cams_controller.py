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


QUERY = """
    SELECT rta.amc_code, 'IIFLWPMS' AS iiflw_pms, rta.user_trxn_no, cm.pan_number, rta.client_name,
    CONCAT(rta.amc_code, '$IIFLWPMS$', rta.user_trxn_no) AS tiff_file_name, NULL AS blank_data, 'NOM' AS nom
    FROM rta_reverse_feed_details rta
    INNER JOIN client_master cm ON cm.client_id = rta.client_id
    WHERE rta.trant_type = 'P' AND (rta.folio_no IS NULL OR rta.folio_no = 0);
"""


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
    #             for file_name in files_in_directory if file_name.startswith(f"CAMNOM{current_date}_")]
    suffixes = [
        # Extract the numeric part before the extension
        int(file_name.split('_')[-1].split('.')[0])
        for file_name in files_in_directory
        if file_name.startswith(f"NOMCAMS{current_date}_")
    ]

    # Increment the filename suffix by finding the maximum value and adding 1
    if suffixes:
        next_suffix = max(suffixes) + 1
    else:
        next_suffix = 1

    # Create the new filename with the incremented suffix
    file_name = f"NOMCAMS{current_date}_{next_suffix}"
    return f'{file_name}.txt'


def get_month_name(month_number):
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY",
                   "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return month_names[month_number - 1]


def get_month_name(month_number):
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY",
                   "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return month_names[month_number - 1]


def get_nominee_cams():
    folder_year = datetime.datetime.now().strftime("%Y")
    folder_month = get_month_name(int(datetime.datetime.now().strftime("%m")))
    folder_day = datetime.datetime.now().strftime("%d")
    main_folder = "nominee"
    sub_folder = f'cams/{folder_year}/{folder_month}/{folder_day}'
    file_name = get_file_name(main_folder, sub_folder)

    try:
        # Establish a connection to the PostgreSQL database
        pool = psql_connect()
        if not pool:
            return make_response(jsonify({"message": "Unable to connect the database."}), http.HTTPStatus.INTERNAL_SERVER_ERROR)

        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cur = ps_connection.cursor()

        # Execute the query
        query = """
        SELECT rta.amc_code, 'IIFLWPMS' AS iiflw_pms, rta.user_trxn_no, cm.pan_number, rta.client_name,
        CONCAT(rta.amc_code, '$IIFLWPMS$', rta.user_trxn_no) AS tiff_file_name, NULL AS blank_data, 'NOM' AS nom
        FROM rta_reverse_feed_details rta
        INNER JOIN client_master cm ON cm.client_id = rta.client_id
        WHERE rta.trant_type = 'P' AND (rta.folio_no IS NULL OR rta.folio_no = 0);
        """

        cur.execute(query)

        # Fetch all the rows returned by the query
        rows = cur.fetchall()

        # Close the cursor and the database connection
        cur.close()
        ps_connection.close()

        if len(rows) < 1:
            return make_response(jsonify({"message": "No new transaction found"}), 404)

        # Create the directories if they do not exist
        # file_path = f'{TRANSACTION_FILE_NAME}/{main_folder}/{sub_folder}/{file_name}'
        folder_path = f'{TRANSACTION_FILE_NAME}/{main_folder}/{sub_folder}'
        # Create the directories if they don't exist
        os.makedirs(folder_path, exist_ok=True)
        # Create the file and write the data

        file_path = f'{folder_path}/{file_name}'
        with open(file_path, 'w', newline='') as f:
            # cur.copy_expert(output_query, f)
            writer = csv.writer(f)
            writer.writerow(["amc_code", "iiflw_pms", "user_trxn_no", "pan_number",
                            "client_name", "tiff_file_name", "blank_data", "nom"])
            writer.writerows(rows)

        # zip_file_name = f'{folder_path}/{folder_day}.zip'
        # with zipfile.ZipFile(zip_file_name, 'a') as zip_file:
        #     zip_file.write(file_path, os.path.basename(file_path))

        # os.remove(file_path)

        # Return the file as a response
        # return send_file(file_path, as_attachment=True)
        # folder_path = f'{TRANSACTION_FILE_NAME}/{main_folder}/{sub_folder}'
        return download_folder(folder_path, f'{folder_day}.zip')

        # return send_file(zip_file_name, as_attachment=True)

    except psycopg2.DatabaseError as error:
        os.remove(file_path)
        return make_response(jsonify({"message": "Please check database connection details"}), http.HTTPStatus.INTERNAL_SERVER_ERROR)


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
