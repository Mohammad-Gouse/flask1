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


def get_month_name(month_number):
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY",
                   "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return month_names[month_number - 1]


def get_nominee_karvy(file_name):
    folder_year = datetime.datetime.now().strftime("%Y")
    folder_month = get_month_name(int(datetime.datetime.now().strftime("%m")))
    folder_day = datetime.datetime.now().strftime("%d")
    main_folder_name = "nominee"
    sub_folder_name = f'karvy/{datetime.datetime.now().strftime("%Y/%B/%d")}'

    try:
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

        folder_path = f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}'
        return download_folder(folder_path, f'{folder_day}.zip')

    except psycopg2.DatabaseError as error:
        print(error)
        os.remove(
            f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{file_name}')
        return make_response(jsonify({"message": "Please check database connection details"}),
                             http.HTTPStatus.INTERNAL_SERVER_ERROR)


def download_folder(folder_path, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Send the zip file as an attachment for download
    return send_file(zip_filename, as_attachment=True)
