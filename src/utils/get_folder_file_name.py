
import os
import zipfile
from flask import Flask, request, jsonify
from src.utils.data_variable import Data_Var
import datetime

TRANSACTION_FILE_NAME = Data_Var.data_store_location


def get_file_name(main, sub_folder, prefix_name):
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
    suffixes = [int(file_name.split('_')[-1])
                for file_name in files_in_directory if file_name.startswith(f"{prefix_name}_")]

    # Increment the filename suffix by finding the maximum value and adding 1
    if suffixes:
        next_suffix = max(suffixes) + 1
    else:
        next_suffix = 1

    # Create the new filename with the incremented suffix
    file_name = f"{prefix_name}_{next_suffix}"
    return file_name
