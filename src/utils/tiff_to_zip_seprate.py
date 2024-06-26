import os
import zipfile
from flask import Flask, request, jsonify
from src.utils.data_variable import Data_Var
TRANSACTION_FILE_NAME = Data_Var.data_store_location


def add_tiff_to_zip(zip_file_path, tiff_data, file_name):
    try:
        print("zip file path", zip_file_path)
        # Create a temporary TIFF file
        temp_tiff_file = "temp_tiff.tiff"
        with open(temp_tiff_file, 'wb') as temp_file:
            temp_file.write(tiff_data)

        file_name = f"{file_name}.tiff"
        print("file_name", file_name)

        folder_name = os.path.splitext(file_name)[0]
        folder_path = os.path.join(zip_file_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Add the temporary TIFF file to the ZIP folder
        with zipfile.ZipFile(os.path.join(folder_path, f"{folder_name}.zip"), 'w') as zip_file:
            zip_file.write(temp_tiff_file, file_name)

        # Remove the temporary TIFF file
        os.remove(temp_tiff_file)

        print("TIFF file added to the ZIP folder successfully.")

    except zipfile.BadZipFile:
        print("Invalid zip file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_tiff_to_zip_api(tiff_data_list, file_name, zip_file_path, zip_prefix):
    try:
        zip_file_path = f'{zip_file_path}/{zip_prefix}.zip'
        print("zip file path", zip_file_path)
        # add_tiff_to_zip(zip_file_path, tiff_data, file_name)

        for idx, tiff_data in enumerate(tiff_data_list):
            # Add each TIFF data to a separate ZIP folder with an index suffix
            folder_name = f"{zip_prefix}_{idx}"
            add_tiff_to_zip(zip_file_path, tiff_data, f"{file_name}_{idx}")

        return jsonify({"message": "TIFF file added to the ZIP folder successfully."}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
