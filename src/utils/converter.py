import os
from flask import request, jsonify
from src.utils import zip_file_process

zip_folder_counter = 1
max_file_size_in_mb = 4


def add_tiff_to_zip_api(tiff_data, file_name, zip_file_path, zip_prefix):
    try:
        # Update the zip_folder_name with the incremented zip_folder_counter
        global zip_folder_counter
        # Initialize zip_folder_name

        zip_folder_name = f"{zip_prefix}{zip_folder_counter}"

        # zip_folder_name = f"{zip_prefix}"
        zip_file_path = f'{zip_file_path}/{zip_folder_name}.zip'

        if os.path.exists(zip_file_path):
            current_zip_file_size = zip_file_process.get_current_zip_file_size(
                zip_file_path)
        else:
            current_zip_file_size = 0

        kb_uploaded_tiff = len(tiff_data) / 1024
        mb_uploaded_tiff = kb_uploaded_tiff / 1024

        # Calculate the total size (current ZIP + uploaded TIFF)
        total_zip_size_mb = current_zip_file_size / \
            (1024 * 1024) + mb_uploaded_tiff

        # Check if the total size exceeds the limit
        if total_zip_size_mb > max_file_size_in_mb:
            # Increment the zip_folder_counter and generate a new zip_folder_name
            zip_folder_counter += 1

            zip_file_path = f'{zip_file_path}/{zip_prefix}{zip_folder_counter}.zip'
            current_zip_file_size = 0  # Reset current ZIP file size to 0

        # Call the add_tiff_to_zip function to add the TIFF data to the ZIP folder
        zip_folder_name = zip_file_process.add_tiff_to_zip(
            tiff_data, file_name, zip_file_path, zip_folder_name=zip_folder_name)

        return jsonify({"message": "TIFF file added to the ZIP folder successfully.", "zip_folder_name": zip_folder_name}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500
