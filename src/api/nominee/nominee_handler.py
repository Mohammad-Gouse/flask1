import shutil
from src.controller import test_excel
from src.utils import dbf_test
import http
import zipfile
import time
import dbf
from datetime import datetime as dt
import requests
from src.controller import rta_reverse_controller, client_master_controller, list_rta_controller, \
    poa_rta_list_controller, poa_upload_controller
from src.controller import nominee_cams_controller, aof_karvy_controller, aof_cams_controller, karvy_reverse_controller, \
    poa_reverse_controller, summary_controller, karvy_reverse_feed_controller
from src.utils import zip_file_process
from src.utils import converter
from src.utils import tiff_to_zip_seprate, pdf_to_tiff, pdf_to_final_tiff, pdf_to_tiff_nominee, tiff_to_zip_nominee, \
    pdf_to_tiff_aof, tiff_to_zip_aof, zip_process_nominee_karvy, zip_process_aof_karvy, file_size_nominee, set_status
from flask import Blueprint, request, jsonify, make_response, send_file, Response
from src.utils import get_folder_file_name
import datetime
import os
import io
import re
import json
import base64
import uuid
import tempfile
from src.utils.data_variable import Data_Var
import pandas as pd
from dotenv import load_dotenv, set_key, get_key
load_dotenv()
# import xlrd

TRANSACTION_FILE_NAME = Data_Var.data_store_location
download = "download"
nominee_handler_bp = Blueprint(
    "nominee_handler", __name__, template_folder="templates")


@nominee_handler_bp.route("/upload-rta", methods=["POST"])
def upload_rta():
    file = request.files.get("file")
    # username = request.get_data("username")
    user = request.form.get("username")
    # print("username: ", username)
    print("user: ", user)

    if file:
        file_extension = file.filename.split('.')[-1].lower()

        print("file extension:", file_extension)

        if file_extension == 'xlsx':
            # Read the XLSX file into a DataFrame
            xls_data = pd.read_excel(file)

            # Convert the DataFrame to CSV in-memory
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'xls':
            # If it's in the older XLS format, read it using xlrd and then convert to CSV
            xls_data = pd.read_excel(file, engine='xlrd')
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'csv':
            # If it's already a CSV file, just read it
            csv_data = file.stream.read().decode(errors="ignore")
        else:
            return "Unsupported file format"

        # Process the CSV data as needed
        return rta_reverse_controller.upload_rta_reverse_feed(
            csv_data.splitlines(), user)

    # if text_file_path is None:
    #     return make_response(jsonify({"message": "No matching records found."}), 200)
    # response = send_file(text_file_path,
    #                      mimetype="application/zip",
    #                      )

    # response.headers['Content-Disposition'] = f'attachment; filename="{text_file_name}.zip"'
    # print(response.headers)
    # return response
    # if isinstance(result, tuple) and len(result) == 2:
    #     zip_file_path, zip_file_name = result
    #     response = send_file(zip_file_path, mimetype="application/zip")
    #     response.headers['Content-Disposition'] = f' filename="{zip_file_name}.zip"'
    #     response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

    #     # print(response.headers)
    #     return response
    # elif result.status_code == 401:
    #     return make_response(jsonify({"message": "Upload a valid file"}), 401)
    # elif result.status_code == 402:
    #     return make_response(jsonify({"message": "Upload client master file"}), 402)
    # else:
    #     return make_response(jsonify({"message": "no record found"}), 400)


@nominee_handler_bp.route("/upload-poa", methods=["POST"])
def upload_poa_api():
    file = request.files.get("file")

    if file:
        file_extension = file.filename.split('.')[-1].lower()

        print("file extension:", file_extension)

        if file_extension == 'xlsx':
            # Read the XLSX file into a DataFrame
            xls_data = pd.read_excel(file)

            # Convert the DataFrame to CSV in-memory
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'xls':
            # If it's in the older XLS format, read it using xlrd and then convert to CSV
            xls_data = pd.read_excel(file, engine='xlrd')
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'csv':
            # If it's already a CSV file, just read it
            csv_data = file.stream.read().decode(errors="ignore")
        else:
            return "Unsupported file format"

        # Process the CSV data as needed
        return poa_upload_controller.upload_poa(csv_data.splitlines())
    # print("path of csv file", zip_filename)
    # if isinstance(dbf_file_path, str):
    #     # If a string is returned, it means there are no matching records
    #     response= send_file(dbf_file_path,mimetype='application/dbase')
    #     response.headers['Content-Disposition'] = f'attachment; filename=f"{dbf_file_name}.dbf"'
    #     print(response.headers)
    #     return response  # Return the "no records found" message
    # else:
    # If a file path is returned, it means there are matching records
    # with zipfile.ZipFile(f'{TRANSACTION_FILE_NAME}/nominee/poa/file.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
    #     zip_file.write(dbf_file_path, arcname=dbf_file_name)
    # response = send_file(zip_filename,
    #                      mimetype="application/zip",
    #                      )

    # response.headers['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
    # print(response.headers)
    # return response
    # print("result: ", result)
    # if isinstance(result, tuple) and len(result) == 2:
    #     zip_file_path, zip_file_name = result
    #     response = send_file(zip_file_path, mimetype="application/zip")
    #     response.headers['Content-Disposition'] = f' filename="{zip_file_name}.zip"'
    #     response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    #
    #     print(response.headers)
    #     return response
    # elif result.status_code == 401:
    #     return make_response(jsonify({"message": "Upload a valid file"}), 401)
    # elif result.status_code == 402:
    #     return make_response(jsonify({"message": "Upload client master file"}), 402)
    # else:
    #     return make_response(jsonify({"message": "no record found"}), 400)


@nominee_handler_bp.route("/upload-client-master", methods=["POST"])
def upload_client_master():
    file = request.files.get("file")

    if file:
        file_extension = file.filename.split('.')[-1].lower()

        print("file extension:", file_extension)

        if file_extension == 'xlsx':
            # Read the XLSX file into a DataFrame
            xls_data = pd.read_excel(file)

            # Convert the DataFrame to CSV in-memory
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'xls':
            # If it's in the older XLS format, read it using xlrd and then convert to CSV
            xls_data = pd.read_excel(file, engine='xlrd')
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'csv':
            # If it's already a CSV file, just read it
            csv_data = file.stream.read().decode(errors="ignore")
        else:
            return "Unsupported file format"

        # Process the CSV data as needed
        return client_master_controller.upload_client_master(csv_data.splitlines())
    # return client_master_controller.upload_client_master(data.splitlines())


@nominee_handler_bp.route("/upload-karvy-reverse", methods=["POST"])
def upload_karvy_reverse():
    file = request.files.get("file")

    if file:
        file_extension = file.filename.split('.')[-1].lower()

        print("file extension:", file_extension)

        if file_extension == 'xlsx':
            # Read the XLSX file into a DataFrame
            xls_data = pd.read_excel(file)

            # Convert the DataFrame to CSV in-memory
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'xls':
            # If it's in the older XLS format, read it using xlrd and then convert to CSV
            xls_data = pd.read_excel(file, engine='xlrd')
            csv_data = xls_data.to_csv(index=False)
        elif file_extension == 'csv':
            # If it's already a CSV file, just read it
            csv_data = file.stream.read().decode(errors="ignore")
        else:
            return "Unsupported file format"

        # Process the CSV data as needed
        return karvy_reverse_feed_controller.upload_karvy_feed(csv_data.splitlines())
    # print (data)
    # result = karvy_reverse_controller.upload_karvy_reverse(
    #     data.splitlines())
    # response = send_file(zip_file_name, mimetype="application/zip",)
    # response.headers['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'

    # print(response.headers)

    # return response
    # if isinstance(result, tuple) and len(result) == 2:
    #     zip_file_path, zip_file_name = result
    #     response = send_file(zip_file_path, mimetype="application/zip")
    #     response.headers['Content-Disposition'] = f'filename="{zip_file_name}.zip"'
    #     response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    #
    #     # print(response.headers)
    #     return response
    # elif result.status_code == 401:
    #     return make_response(jsonify({"message": "Upload a valid file"}), 401)
    # else:
    #     return make_response(jsonify({"message": "no record found"}), 400)


@nominee_handler_bp.route('/list-rta', methods=['GET'])
def get_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return list_rta_controller.get_list_rta(page, per_page)


@nominee_handler_bp.route('/poa-list-rta', methods=['GET'])
def get_poa_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return poa_rta_list_controller.get_poa_list_rta(page, per_page)

# Old transactions


@nominee_handler_bp.route('/list-rta-nom', methods=['GET'])
def get_list_nom():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return list_rta_controller.get_list_rta_nom(page, per_page)


@nominee_handler_bp.route('/list-rta-nom-old', methods=['GET'])
def get_list_nom_old():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return list_rta_controller.get_list_rta_nom_old(page, per_page)


@nominee_handler_bp.route('/list-rta-old', methods=['GET'])
def get_list_old():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return list_rta_controller.get_list_rta_old(page, per_page)


@nominee_handler_bp.route('/poa-list-rta-old', methods=['GET'])
def get_poa_list_old():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    return poa_rta_list_controller.get_poa_list_rta_old(page, per_page)


@nominee_handler_bp.route("/nominee-cams", methods=["GET"])
def get_nominee_cams():
    return nominee_cams_controller.get_nominee_cams()


@nominee_handler_bp.route("/aof-cams", methods=["GET"])
def get_aof_cams():
    # file_name = request.args.get('filename')
    return aof_cams_controller.get_aof_cams("file_name")


@nominee_handler_bp.route("/aof-karvy", methods=["GET"])
def get_aof_karvy():
    return aof_karvy_controller.get_aof_karvy()


# @nominee_handler_bp.route('/nominee-karvy-converter', methods=['POST'])
# def nominee_karvy_converter_api():
#     # data = request.form.to_dict()
#     # pdf_base64_list = data.get('pdf_files')
#     pdf_file_path = "C:/Python/1sample.pdf"
#     pdf_base64_list = pdf_to_data_uri(pdf_file_path)
#     global filename
#     temp_folder = "temp_folder"

#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)

#     if not pdf_base64_list:
#         return jsonify({"error": "No PDF files provided."}), 400
#     saved_pdf_path = []
#     # for base64_string in pdf_base64_list:
#     try:
#         # Decode Base64 data and save it as a PDF file
#         decoded_data = base64.b64decode(pdf_base64_list)

#         # path
#         if decoded_data is not None:
#             filename = 'file{}.pdf'.format(str(uuid.uuid4()))
#         pdf_path = os.path.join(f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
#         with open(pdf_path, 'wb') as f:
#             f.write(decoded_data)
#         saved_pdf_path.append(pdf_path)
#         tiff_file_list = zip_process_nominee_karvy.process_multiple_pdfs(saved_pdf_path)
#         response = zip_process_nominee_karvy.add_tiff_to_zip_api(tiff_file_list, 'output_folder')

#         return jsonify(response)
#     except Exception as e:
#         # Handle exceptions here if needed
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Delete the temporary TIFF files and the temp_folder
#         temp_folder_path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#         if os.path.exists(temp_folder_path):
#             for file_name in os.listdir(temp_folder_path):
#                 file_path = os.path.join(temp_folder_path, file_name)
#                 os.remove(file_path)
#             os.rmdir(temp_folder_path)


# @nominee_handler_bp.route('/aof-cams-converter', methods=['POST'])
# def aof_cams_converter_api():
#     temp_folder = "temp_folder"
#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)
#     folder_year = datetime.datetime.now().strftime("%Y")
#     folder_month = get_month_name(int(datetime.datetime.now().strftime("%m")))
#     folder_day = datetime.datetime.now().strftime("%d")
#     saved_pdf_paths = []
#     try:
#         for index in range(0, 7):  # Assuming there are 6 files (pdf_file1, pdf_file2, ..., pdf_file6)
#             key = f'pdf_file{index}'
#             base64_string = request.form.get(key)

#             if base64_string:
#                 # Decode the base64 data and save it as a PDF file
#                 decoded_data = base64.b64decode(base64_string.split(',')[1])
#                 filename = f'file_{str(uuid.uuid4())}.pdf'
#                 pdf_path = os.path.join(f'{TRANSACTION_FILE_NAME}/{temp_folder}/', filename)
#                 with open(pdf_path, 'wb') as f:
#                     f.write(decoded_data)
#                 saved_pdf_paths.append(pdf_path)

#         # Process the saved PDF files into TIFF format
#         overall_output_folder = f'{TRANSACTION_FILE_NAME}/aof/cams/{folder_year}/{folder_month}/{folder_day}'
#         tiff_file_list = pdf_to_tiff_aof.process_multiple_pdfs(saved_pdf_paths)
#         response = tiff_to_zip_aof.add_tiff_to_zip_api(tiff_file_list, 'output_folder')
#         return jsonify(response), 200

#     except Exception as e:
#         # Handle exceptions here if needed
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Delete the temporary PDF files and the temp_folder after processing
#         for pdf_file in saved_pdf_paths:
#             os.remove(pdf_file)

#         if os.path.exists(path):
#             os.rmdir(path)


# @nominee_handler_bp.route('/nominee-cams-converter', methods=['POST'])
# def nomineee_cams_converter():
#     data = request.form.to_dict()
#     pdf_base64_list = data.get('pdf_files')
#     # pdf_file_path = "C:/Python/1sample.pdf"
#     # pdf_base64_list = pdf_to_data_uri(pdf_file_path)
#     global filename
#     temp_folder = "temp_folder"

#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)

#     if not pdf_base64_list:
#         return jsonify({"error": "No PDF files provided."}), 400
#     saved_pdf_path = []
#     # for base64_string in pdf_base64_list:
#     try:
#         # Decode Base64 data and save it as a PDF file
#         decoded_data = base64.b64decode(pdf_base64_list.split(',')[1])

#         # path
#         if decoded_data is not None:
#             filename = 'file{}.pdf'.format(str(uuid.uuid4()))
#         pdf_path = os.path.join(f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
#         with open(pdf_path, 'wb') as f:
#             f.write(decoded_data)
#         saved_pdf_path.append(pdf_path)
#         tiff_file_list = pdf_to_tiff_nominee.process_multiple_pdfs(saved_pdf_path)
#         response = tiff_to_zip_nominee.add_tiff_to_zip_api(tiff_file_list, 'output_folder')

#         return jsonify(response)
#     except Exception as e:
#         # Handle exceptions here if needed
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Delete the temporary TIFF files and the temp_folder
#         temp_folder_path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#         if os.path.exists(temp_folder_path):
#             for file_name in os.listdir(temp_folder_path):
#                 file_path = os.path.join(temp_folder_path, file_name)
#                 os.remove(file_path)
#             os.rmdir(temp_folder_path)


# @nominee_handler_bp.route('/aof-karvy-converter', methods=['POST'])
# def aof_karvy_converter_api():
#     temp_folder = "temp_folder"
#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)
#     folder_year = datetime.datetime.now().strftime("%Y")
#     folder_month = get_month_name(int(datetime.datetime.now().strftime("%m")))
#     folder_day = datetime.datetime.now().strftime("%d")
#     saved_pdf_paths = []
#     try:
#         for index in range(0, 7):  # Assuming there are 6 files (pdf_file1, pdf_file2, ..., pdf_file6)
#             key = f'pdf_file{index}'
#             base64_string = request.form.get(key)

#             if base64_string:
#                 # Decode the base64 data and save it as a PDF file
#                 decoded_data = base64.b64decode(base64_string.split(',')[1])
#                 filename = f'file_{str(uuid.uuid4())}.pdf'
#                 pdf_path = os.path.join(f'{TRANSACTION_FILE_NAME}/{temp_folder}/', filename)
#                 with open(pdf_path, 'wb') as f:
#                     f.write(decoded_data)
#                 saved_pdf_paths.append(pdf_path)

#         # Process the saved PDF files into TIFF format
#         overall_output_folder = f'{TRANSACTION_FILE_NAME}/aof/cams/{folder_year}/{folder_month}/{folder_day}'
#         tiff_file_list = zip_process_aof_karvy.process_multiple_pdfs(saved_pdf_paths)
#         response = zip_process_aof_karvy.add_tiff_to_zip_api(tiff_file_list, 'output_folder')
#         return jsonify(response), 200

#     except Exception as e:
#         # Handle exceptions here if needed
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Delete the temporary PDF files and the temp_folder after processing
#         for pdf_file in saved_pdf_paths:
#             os.remove(pdf_file)

#         if os.path.exists(path):
#             os.rmdir(path)


def get_month_name(month_number):
    month_names = ["JAN", "FEB", "MAR", "APR", "MAY",
                   "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return month_names[month_number - 1]


# @nominee_handler_bp.route('/poa-converter', methods=['POST'])
# def poa_converter():
#     temp_folder = "temp_folder"
#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)

#     saved_pdf_paths = []
#     try:
#         for index in range(0, 7):  # Assuming there are 6 files (pdf_file1, pdf_file2, ..., pdf_file6)
#             key = f'pdf_file{index}'
#             base64_string = request.form.get(key)

#             if base64_string:
#                 # Decode the base64 data and save it as a PDF file
#                 decoded_data = base64.b64decode(base64_string.split(',')[1])
#                 filename = f'file_{str(uuid.uuid4())}.pdf'
#                 pdf_path = os.path.join(f'{TRANSACTION_FILE_NAME}/{temp_folder}/', filename)
#                 with open(pdf_path, 'wb') as f:
#                     f.write(decoded_data)
#                 saved_pdf_paths.append(pdf_path)

#         # Process the saved PDF files into TIFF format
#         overall_output_folder = f'{TRANSACTION_FILE_NAME}/nominee/poa/{datetime.datetime.now().strftime("%Y/%B/%d")}'
#         tiff_file_list = pdf_to_final_tiff.process_multiple_pdfs(saved_pdf_paths, overall_output_folder)

#         return make_response(
#             {"message": " pdf to single tiff successfully "}
#         )


#     except Exception as e:
#         # Handle exceptions here if needed
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Delete the temporary PDF files and the temp_folder after processing
#         for pdf_file in saved_pdf_paths:
#             os.remove(pdf_file)

#         if os.path.exists(path):
#             os.rmdir(path)


# @nominee_handler_bp.route('/nominnee-cams-converter', methods=['POST'])
# def nominee_cams_converter():
#     data = request.form.to_dict()
#     pdf_base64_list = data.get('pdf_files')
#     # pdf_file_path = "C:/Python/1sample.pdf"
#     # pdf_base64_list = pdf_to_data_uri(pdf_file_path)
#     global filename
#     temp_folder = "temp_folder"

#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)

#     if not pdf_base64_list:
#         return jsonify({"error": "No PDF files provided."}), 400
#     saved_pdf_path = []
#     # for base64_string in pdf_base64_list:
#     try:
#         # Decode Base64 data and save it as a PDF file
#         decoded_data = base64.b64decode(pdf_base64_list).decode('utf-8')

#         # path
#         if decoded_data is not None:
#             filename = 'file{}.pdf'.format(str(uuid.uuid4()))
#         pdf_path = os.path.join(f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
#         with open(pdf_path, 'wb') as f:
#             f.write(decoded_data)
#         saved_pdf_path.append(pdf_path)
#         tiff_file_list = pdf_to_tiff_nominee.process_multiple_pdfs(saved_pdf_path)
#         response = tiff_to_zip_nominee.add_tiff_to_zip_api(tiff_file_list, 'output_folder')

#         return jsonify(response)
#     except Exception as e:
#         # Handle exceptions here if needed
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Delete the temporary TIFF files and the temp_folder
#         temp_folder_path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#         if os.path.exists(temp_folder_path):
#             for file_name in os.listdir(temp_folder_path):
#                 file_path = os.path.join(temp_folder_path, file_name)
#                 os.remove(file_path)
#             os.rmdir(temp_folder_path)


def pdf_to_data_uri(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        pdf_data = f.read()
        base64_string = base64.b64encode(pdf_data).decode('utf-8')
        data_uri = f'data:application/pdf;base64,{base64_string}'

        return data_uri


# def decode_base64_pdf(base64_string):
#     # Use regex to extract the base64 encoded data
#     match = re.search(r'base64,(.*)', base64_string)
#     base64_string = base64_string.replace("\n", "").replace(" ", "")

#     if match:
#         base64_data = match.group(1)
#         try:
#             decoded_data = base64.b64decode(base64_data)
#             return decoded_data
#         except base64.binascii.Error as e:
#              print("Base64 decoding error:", e)
#              return None
#     else:
#         return None

# @nominee_handler_bp.route('/testing',methods=['POST'])
# def testing():
#         # i=1
#         # data = request.form
#         # pdf_base64_list = data.getlist('pdf_files')
#         pdf_paths=request.get_json().get('pdf_files')
#         # pdf_file_path="C:/Python/1sample.pdf"
#         # pdf_base64_list=pdf_to_data_uri(pdf_file_path)

#         if not pdf_paths:
#             return jsonify({"error": "No PDF files provided."}), 400

#         saved_pdf_info = []
#         for pdf_path in pdf_paths:
#             try:
#                 base64_string=pdf_to_data_uri(pdf_path)
#                 # Decode Base64 data and save it as a PDF file
#                 decoded_data = base64.b64decode(base64_string)
#                 # path
#                 # temp_folder = tempfile.mkdtemp()
#                 filename = 'file{}.pdf'.format(str(uuid.uuid4()))
#                 pdf_path = os.path.join("C:/Users/viral dangar/OneDrive/Desktop/IFL/mf-utility-be/data/temp_folder", filename)

#                 with open(pdf_path, 'wb') as f:
#                     f.write(decoded_data)
#                     # path="C:/Users/viral dangar/OneDrive/Desktop/iifl_poc/mf-utility-be"
#                     # f.save(os.path.join("D:/Utility_dev/mf-utility-be/src/data/pdf_file.pdf"))
#                 pdf_size = os.path.getsize(pdf_path)  # Get the size of the PDF file in bytes
#                 saved_pdf_info.append({"filename": filename, "size": pdf_size})
#                 # i+=1
#             except Exception as e:
#                 print("Error saving PDF:", e)

#         return jsonify({"pdf_info": saved_pdf_info})

def remove_temp_folder(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(folder_path)


@nominee_handler_bp.route('/poa-converter', methods=['POST'])
def poa_converter():
    pdf_file_name = request.form.get('file_name')
    import re
    special_characters_pattern = r"[^a-zA-Z0-9. _-]"
    if re.search(special_characters_pattern, pdf_file_name):
        return make_response(jsonify({"message": "Can't able to create Tiff file name beacause of Invalid data got uploaded. Please Check the data of 'folio number','AMC code', or 'usrtrxno' file name contains special characters other than '.', ' ', '_', and '-'."}), 400)
    temp_folder = f'temp_folder_{pdf_file_name}'
    id = request.form.get('id')
    path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
    if not os.path.exists(path):
        os.makedirs(path)

    pdf_info = []
    try:
        # Create a temporary directory to store uploaded files
        # Loop through the pdf_file1 to pdf_file6 fields
        for i in range(1, 8):
            pdf_field_name = f'pdf_file{i}'
            pdf_file = request.files.get(pdf_field_name)

            if pdf_file:
                # Get file info
                filename = pdf_file.filename
                file_content = pdf_file.read()
                # Save the PDF file to the temporary directory
                temp_file_path = os.path.join(
                    f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_content)
                    pdf_info.append(temp_file_path)
                # Process the file or gather its info
                # ...

        overall_output_folder = f'{TRANSACTION_FILE_NAME}/nominee/poa/'
        tiff_file_list, tiff_file_sizes = pdf_to_final_tiff.process_multiple_pdfs(
            pdf_info, overall_output_folder, pdf_file_name)  # Use the function directly
        # zip_file_path, tiff_filename = pdf_to_final_tiff.convert_tiff_to_zip(
        #     tiff_file_list, pdf_file_name)
        # response = send_file(zip_file_path, mimetype='application/zip')
        # zip_file_name = f'{pdf_file_name}.zip'
        # response.headers['Content-Disposition'] = f' filename="{zip_file_name}"'
        # response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        size = tiff_file_sizes / 1000
        tiff_file_size = file_size_nominee.tiff_file_size_poa(id, size)
        poa_status = set_status.poa_status_set(id)

        return make_response(jsonify({"message": "Tiff file generated successfully and size is "}),
                             200)

        # print(response.headers)
        # return response
    except FileNotFoundError as e:
        return jsonify({"error": "File not found."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the temporary PDF files and the temp_folder after processing
        if os.path.exists(path):
            try:
                # Iterate over all files in the directory and remove them
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                # After all files are removed, remove the empty directory
                os.rmdir(path)
            except Exception as e:
                print(f"Error while deleting temp folder: {e}")


@nominee_handler_bp.route('/nominee-cams-converter', methods=['POST'])
def nomineee_cams_converter():
    pdf_file_name = request.form.get('file_name')
    id = request.form.get('id')
    temp_folder = f'temp_folder_{pdf_file_name}'
    path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
    if not os.path.exists(path):
        os.makedirs(path)

    pdf_info = []
    try:
        # Create a temporary directory to store uploaded files
        # Loop through the pdf_file1 to pdf_file6 fields
        for i in range(1, 2):
            pdf_field_name = f'pdf_file{i}'
            pdf_file = request.files.get(pdf_field_name)

            if pdf_file:
                # Get file info
                filename = pdf_file.filename
                file_content = pdf_file.read()
                # Save the PDF file to the temporary directory
                temp_file_path = os.path.join(
                    f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_content)
                    pdf_info.append(temp_file_path)
                # Process the file or gather its info
                # ...

        overall_output_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/'
        tiff_file_path, tiff_file_sizes = pdf_to_tiff_nominee.process_multiple_pdfs(
            pdf_info, overall_output_folder, pdf_file_name)  # Use the function directly
        size = tiff_file_sizes/1000
        tiff_file_size = file_size_nominee.tiff_file_size_set(id, size)
        nom_status = set_status.nominee_status_set(id)

        return make_response(jsonify({"message": "Tiff file generated successfully and size is "}),
                             200)

    except FileNotFoundError as e:
        return jsonify({"error": "File not found."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the temporary PDF files and the temp_folder after processing

        if os.path.exists(path):
            try:
                # Iterate over all files in the directory and remove them
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                # After all files are removed, remove the empty directory
                os.rmdir(path)
            except Exception as e:
                print(f"Error while deleting temp folder: {e}")


# @nominee_handler_bp.route('/nominee-karvy-converter', methods=['POST'])
# def nominee_karvy_converter_api():
#     pdf_file_name = request.form.get('file_name')
#     id = request.form.get('id')
#     temp_folder = f'temp_folder_{pdf_file_name}'
#     path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
#     if not os.path.exists(path):
#         os.makedirs(path)

#     pdf_info = []
#     try:
#         # Create a temporary directory to store uploaded files
#         # Loop through the pdf_file1 to pdf_file6 fields
#         for i in range(1, 2):
#             pdf_field_name = f'pdf_file{i}'
#             pdf_file = request.files.get(pdf_field_name)

#             if pdf_file:
#                 # Get file info
#                 filename = pdf_file.filename
#                 file_content = pdf_file.read()
#                 # Save the PDF file to the temporary directory
#                 temp_file_path = os.path.join(
#                     f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
#                 with open(temp_file_path, 'wb') as temp_file:
#                     temp_file.write(file_content)
#                     pdf_info.append(temp_file_path)
#                 # Process the file or gather its info
#                 # ...

#         overall_output_folder = f'{TRANSACTION_FILE_NAME}/nominee/karvy/'
#         tiff_file_list, tiff_file_sizes = zip_process_nominee_karvy.process_multiple_pdfs(
#             pdf_info, overall_output_folder, pdf_file_name)  # Use the function directly
#         # zip_file_path, tiff_filename = zip_process_nominee_karvy.convert_tiff_to_zip(
#         #     tiff_file_list, pdf_file_name)
#         size = tiff_file_sizes/1000
#         print("size: ", size)
#         tiff_file_size = file_size_nominee.tiff_file_size_set(id, size)
#         nom_status = set_status.nominee_status_set(id)

#         return make_response(jsonify({"message": "Tiff file generated successfully "}),
#                              200)

#         # response = send_file(zip_file_path, mimetype='application/zip')
#         # zip_file_name = f'{pdf_file_name}.zip'
#         # response.headers['Content-Disposition'] = f' filename="{zip_file_name}"'
#         # response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
#         #
#         # return response
#     except FileNotFoundError as e:
#         return jsonify({"error": "File not found."}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         # Delete the temporary PDF files and the temp_folder after processing

#         if os.path.exists(path):
#             try:
#                 # Iterate over all files in the directory and remove them
#                 for file_name in os.listdir(path):
#                     file_path = os.path.join(path, file_name)
#                     if os.path.isfile(file_path):
#                         os.remove(file_path)

#                 # After all files are removed, remove the empty directory
#                 os.rmdir(path)
#             except Exception as e:
#                 print(f"Error while deleting temp folder: {e}")

@nominee_handler_bp.route('/nominee-karvy-converter', methods=['POST'])
def nominee_karvy_converter_api():
    pdf_file_name = request.form.get('file_name')
    id = request.form.get('id')
    temp_folder = f'temp_folder_{pdf_file_name}'
    path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
    if not os.path.exists(path):
        os.makedirs(path)

    pdf_info = []
    try:
        # Create a temporary directory to store uploaded files
        # Loop through the pdf_file1 to pdf_file6 fields
        for i in range(1, 2):
            pdf_field_name = f'pdf_file{i}'
            pdf_file = request.files.get(pdf_field_name)

            if pdf_file:
                # Get file info
                filename = pdf_file.filename
                file_content = pdf_file.read()
                # Save the PDF file to the temporary directory
                temp_file_path = os.path.join(
                    f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_content)
                    pdf_info.append(temp_file_path)
                # Process the file or gather its info
                # ...

        overall_output_folder = f'{TRANSACTION_FILE_NAME}/nominee/karvy/'
        tiff_file_list, tiff_file_sizes = zip_process_nominee_karvy.process_multiple_pdfs(
            pdf_info, overall_output_folder, pdf_file_name)  # Use the function directly
        # zip_file_path, tiff_filename = zip_process_nominee_karvy.convert_tiff_to_zip(
        #     tiff_file_list, pdf_file_name)
        size = tiff_file_sizes/1000
        print("size: ", size)
        tiff_file_size = file_size_nominee.tiff_file_size_set(id, size)
        nom_status = set_status.nominee_status_set(id)

        return make_response(jsonify({"message": "Tiff file generated successfully "}),
                             200)

        # response = send_file(zip_file_path, mimetype='application/zip')
        # zip_file_name = f'{pdf_file_name}.zip'
        # response.headers['Content-Disposition'] = f' filename="{zip_file_name}"'
        # response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        #
        # return response
    except FileNotFoundError as e:
        return jsonify({"error": "File not found."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the temporary PDF files and the temp_folder after processing

        if os.path.exists(path):
            try:
                # Iterate over all files in the directory and remove them
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                # After all files are removed, remove the empty directory
                os.rmdir(path)
            except Exception as e:
                print(f"Error while deleting temp folder: {e}")


@nominee_handler_bp.route('/aof-karvy-converter', methods=['POST'])
def aof_karvy_converter_api():
    pdf_file_name = request.form.get('file_name')
    temp_folder = f'temp_folder_{pdf_file_name}'
    id = request.form.get('id')

    path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
    if not os.path.exists(path):
        os.makedirs(path)

    pdf_info = []
    try:
        # Create a temporary directory to store uploaded files
        # Loop through the pdf_file1 to pdf_file6 fields
        for i in range(1, 6):
            pdf_field_name = f'pdf_file{i}'
            pdf_file = request.files.get(pdf_field_name)

            if pdf_file:
                # Get file info
                filename = pdf_file.filename
                file_content = pdf_file.read()
                # Save the PDF file to the temporary directory
                temp_file_path = os.path.join(
                    f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_content)
                    pdf_info.append(temp_file_path)
                # Process the file or gather its info
                # ...

        overall_output_folder = f'{TRANSACTION_FILE_NAME}/aof/karvy/'
        tiff_file_list, tiff_file_sizes = zip_process_aof_karvy.process_multiple_pdfs(
            pdf_info, overall_output_folder, pdf_file_name)  # Use the function directly
        # zip_file_path, tiff_filename = zip_process_aof_karvy.convert_tiff_to_zip(
        #     tiff_file_list, pdf_file_name)
        # response = send_file(zip_file_path, mimetype='application/zip')
        # zip_file_name = f'{pdf_file_name}.zip'
        # response.headers['Content-Disposition'] = f' filename="{zip_file_name}"'
        # response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        #
        # return response
        size = tiff_file_sizes / 1000
        tiff_file_size = file_size_nominee.tiff_file_size_set_aof(id, size)
        aof_status = set_status.aof_status_set(id)

        return make_response(jsonify({"message": "Tiff file generated successfully "}),
                             200)
    except FileNotFoundError as e:
        return jsonify({"error": "File not found."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the temporary PDF files and the temp_folder after processing

        if os.path.exists(path):
            try:
                # Iterate over all files in the directory and remove them
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                # After all files are removed, remove the empty directory
                os.rmdir(path)
            except Exception as e:
                print(f"Error while deleting temp folder: {e}")


@nominee_handler_bp.route('/aof-cams-converter', methods=['POST'])
def aof_cams_converter_api():
    pdf_file_name = request.form.get('file_name')
    temp_folder = f'temp_folder_{pdf_file_name}'
    id = request.form.get('id')

    path = f'{TRANSACTION_FILE_NAME}/{temp_folder}'
    if not os.path.exists(path):
        os.makedirs(path)

    pdf_info = []
    try:
        # Create a temporary directory to store uploaded files
        # Loop through the pdf_file1 to pdf_file6 fields
        for i in range(1, 6):
            pdf_field_name = f'pdf_file{i}'
            pdf_file = request.files.get(pdf_field_name)

            if pdf_file:
                # Get file info
                filename = pdf_file.filename
                file_content = pdf_file.read()
                # Save the PDF file to the temporary directory
                temp_file_path = os.path.join(
                    f'{TRANSACTION_FILE_NAME}/{temp_folder}', filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_content)
                    pdf_info.append(temp_file_path)
                # Process the file or gather its info
                # ...

        overall_output_folder = f'{TRANSACTION_FILE_NAME}/aof/cams/'
        tiff_file_list, tiff_file_sizes = pdf_to_tiff_aof.process_multiple_pdfs(
            pdf_info, overall_output_folder, pdf_file_name)  # Use the function directly

        # zip_file_path, tiff_filename = tiff_to_zip_aof.convert_tiff_to_zip(
        #     tiff_file_list, pdf_file_name)
        # zip_file_name = f'CAMS_RIA_{pdf_file_name}.zip'
        # response = send_file(zip_file_path, mimetype='application/zip')
        # response.headers['Content-Disposition'] = f' filename="{zip_file_name}"'
        # response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        # return response
        size = tiff_file_sizes / 1000
        tiff_file_size = file_size_nominee.tiff_file_size_set_aof(id, size)
        nom_status = set_status.aof_status_set(id)

        return make_response(jsonify({"message": "Tiff file generated successfully "}),
                             200)

    except FileNotFoundError as e:
        return jsonify({"error": "File not found."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the temporary PDF files and the temp_folder after processing

        if os.path.exists(path):
            try:
                # Iterate over all files in the directory and remove them
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                # After all files are removed, remove the empty directory
                os.rmdir(path)
            except Exception as e:
                print(f"Error while deleting temp folder: {e}")


@nominee_handler_bp.route("/poa-summary", methods=["GET"])
def get_poa_summary():
    data = request.args.to_dict()
    result = summary_controller.get_poa_summary(data)

    if result.status_code == 200:
        return result
    elif result.status_code == 404:
        return make_response(jsonify({"message": "Please change the date, no data availabe in given range"}), 404)
    else:
        return make_response(jsonify({"message": "Database error"}), 500)


@nominee_handler_bp.route("/rta-summary", methods=["GET"])
def get_rta_summary():
    data = request.args.to_dict()
    result = summary_controller.get_rta_summary(data)

    if result.status_code == 200:
        return result
    elif result.status_code == 404:
        return make_response(jsonify({"message": "Please change the date, no data availabe in given range"}), 404)
    else:
        return make_response(jsonify({"message": "Database error"}), 500)


# @nominee_handler_bp.route("/download-zip-cams", methods=["POST"])
# def download_zip():
#     try:
#         data = request.get_json()
#         # print("json",data)
#         # # Assuming you're sending data as form-data
#         nominee_files = data.get("cams_tiff_file", [])
#         text_files = data.get("cams_text_file", [])
#         print(text_files)
#         # nominee_files = request.files.getlist("cams_tiff_file")
#         # text_files = request.files.getlist("cams_text_file")
#         # nominee_files = request.form.get("cams-tiff-file")
#         # text_files = request.form.get("cams-text-file")
#         tiff = request.form.get("cams-tiff-file")
#         print("nvkjvndjv", tiff)
#         print("tiff", nominee_files)
#
#         # reg_code = request.form.get("reg_code").lower()
#
#         nominee_cams_path = os.path.join(TRANSACTION_FILE_NAME, "nominee", "cams")
#         output_path = os.path.join(TRANSACTION_FILE_NAME, "output")
#
#         if not os.path.exists(output_path):
#             os.makedirs(output_path)
#
#         time = generate_file_name_with_epoch()
#         nominee_zip_filename = f'cams_nom_{time}.zip'
#
#         # Create the ZIP file with nominee files
#         create_zip_file(nominee_zip_filename, nominee_files, nominee_cams_path)
#
#         # Create text files from 'cams-text-file' data and save them with epoch time
#         text_file_name = create_text_files(text_files, time, output_path)
#
#         # Create a final ZIP file with both nominee ZIP and text files
#         final_zip_filename = f'cams_nom_{time}.zip'
#         create_combined_zip_file(final_zip_filename, nominee_zip_filename, text_file_name, output_path)
#         response = send_file(os.path.join(output_path, final_zip_filename))
#         response.headers['Content-Disposition'] = f' filename="{final_zip_filename}.zip"'
#         response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
#
#         return response
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#
# def create_zip_file(zip_filename, files_to_include, directory):
#     # Ensure that the base directory exists or create it if it doesn't
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#
#     with zipfile.ZipFile(os.path.join(directory, zip_filename), 'w', zipfile.ZIP_DEFLATED) as zipf:
#         # Add TIFF files to the ZIP file
#         print("include", files_to_include)
#         for file in files_to_include:
#             print("files", file)
#             if file.endswith(".tiff"):
#                 file_path = os.path.join(directory, file.filename)
#                 file.save(file_path)
#                 # Use os.path.relpath to get the relative path within the ZIP file
#                 zipf.write(file_path, os.path.relpath(file_path, directory))
#                 os.remove(file_path)
#
#
# # def create_text_files(text_files, time, directory):
# #     # Create text files and save them with epoch time
# #     if not os.path.exists(directory):
# #         os.makedirs(directory)
# #
# #     for i, text_file in enumerate(text_files):
# #         text_filename = f'cams_nom_{time}_{i}.txt'
# #         text_file_path = os.path.join(directory, text_filename)
# #         text_file.save(text_file_path)
#
#
# def create_combined_zip_file(final_zip_filename, nominee_zip_filename, text_files, directory):
#     # Create a final ZIP file containing the nominee ZIP and text files
#     with zipfile.ZipFile(os.path.join(directory, final_zip_filename), 'w', zipfile.ZIP_DEFLATED) as zipf:
#         # Add nominee ZIP file to the final ZIP
#         zipf.write(os.path.join(directory, nominee_zip_filename), nominee_zip_filename)
#
#         # Add text files to the final ZIP
#         for text_file in text_files:
#             text_filename = text_file.filename
#             text_file_path = os.path.join(directory, text_filename)
#             zipf.write(text_file_path, os.path.relpath(text_file_path, directory))
#             os.remove(text_file_path)
#
#
def generate_file_name_with_epoch():
    current_time = int(time.time())
    return current_time


#
#
# def create_text_files(text_files, time, directory):
#     # Create text files and save them with epoch time
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     text_filename = f'cams_nom_{time}.txt'
#     # Assuming 'text_files' is a list of strings
#     for text_data in enumerate(text_files):
#         text_file_path = os.path.join(directory, text_filename)
#
#         # Create and write the text data to the text file with commas and newlines
#         with open(text_file_path, 'w') as text_file:
#             formatted_text = ',\n'.join(text_data)  # Join the list items with commas and newlines
#             text_file.write(formatted_text)
#
#     return text_filename
@nominee_handler_bp.route("/download-cams-zip", methods=["POST"])
def donwload_cams_zip():
    try:
        data = request.get_json()
        nominee_files = data.get("cams_tiff_file", [])
        text_files = data.get("cams_text_file", [])
        id = data.get("id", [])
        print("idsss", id)
        print("nominee_files", nominee_files)

        output_folder = f'{TRANSACTION_FILE_NAME}/output'
        path = f'{TRANSACTION_FILE_NAME}/nominee/cams'
        response_file_path = create_combined_zip_cams(
            nominee_files, text_files, path, output_folder)
        ids = file_size_nominee.download_on_nominee(id)
        response = send_file(response_file_path, mimetype="application/zip")
        time = generate_file_name_with_epoch()
        response.headers['Content-Disposition'] = f' filename="CAMS_NOM_{time}.zip"'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@nominee_handler_bp.route("/download-aof-cams-zip", methods=["POST"])
def donwload_aof_zip():
    try:
        data = request.get_json()
        nominee_files = data.get("cams_tiff_file", [])
        text_files = data.get("cams_text_file", [])
        id = data.get("id", [])
        print("nominee_files", nominee_files)

        output_folder = f'{TRANSACTION_FILE_NAME}/output'
        path = f'{TRANSACTION_FILE_NAME}/aof/cams'
        response_file_path = create_combined_zip_aof(
            nominee_files, text_files, path, output_folder)
        ids = file_size_nominee.download_on_aof(id)
        response = send_file(response_file_path, mimetype="application/zip")
        time = generate_file_name_with_epoch()
        response.headers['Content-Disposition'] = f' filename="CAMS_RIA_{time}.zip"'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@nominee_handler_bp.route("/download-aof-karvy-zip", methods=["POST"])
def donwload_aof_karvy_zip():
    try:
        data = request.get_json()
        nominee_files = data.get("cams_tiff_file", [])
        text_files = data.get("cams_text_file", [])
        id = data.get("id", [])
        print("nominee_files", nominee_files)
        formatted_date = current_date.strftime("%d%m%y")

        output_folder = f'{TRANSACTION_FILE_NAME}/output'
        path = f'{TRANSACTION_FILE_NAME}/aof/karvy'
        response_file_path = create_combined_zip_aof_karvy(
            nominee_files, text_files, path, output_folder)
        ids = file_size_nominee.download_on_aof(id)
        response = send_file(response_file_path, mimetype="application/zip")
        time = generate_file_name_with_epoch()
        response.headers[
            'Content-Disposition'] = f' filename="INP000005874_{formatted_date}_{time}.zip"'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@nominee_handler_bp.route("/download-nominee-karvy-zip", methods=["POST"])
def donwload_nominee_karvy_zip():
    try:
        data = request.get_json()
        nominee_files = data.get("cams_tiff_file", [])
        zip_file = data.get("zip_name")
        id = data.get("id", [])
        # text_files = data.get("cams_text_file", [])
        print("nominee_files", nominee_files)

        output_folder = f'{TRANSACTION_FILE_NAME}/output'
        path = f'{TRANSACTION_FILE_NAME}/nominee/karvy'
        response_file_path = create_combined_zip_karvy_nominee(
            nominee_files, path, output_folder, zip_file)
        response = send_file(response_file_path, mimetype="application/zip")
        ids = file_size_nominee.download_on_nominee(id)
        time = generate_file_name_with_epoch()
        response.headers['Content-Disposition'] = f' filename="{zip_file}TRXN001.zip"'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@nominee_handler_bp.route("/download-poa-zip", methods=["POST"])
def donwload_poa_zip():
    try:
        data = request.get_json()
        nominee_files = data.get("cams_tiff_file", [])
        text_files = data.get("cams_text_file", [])
        id = data.get("id", [])
        print("nominee_files", nominee_files)
        formatted_date = current_date.strftime("%y%m%d")

        output_folder = f'{TRANSACTION_FILE_NAME}/output'
        path = f'{TRANSACTION_FILE_NAME}/nominee/poa'
        response_file_path = create_combined_zip_poa(
            nominee_files, text_files, path, output_folder)
        ids = file_size_nominee.download_on_poa(id)
        response = send_file(response_file_path, mimetype="application/zip")
        time = generate_file_name_with_epoch()
        response.headers['Content-Disposition'] = f' filename="POA.zip"'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_combined_zip_cams(nominee_files, text_files_data, path_for_tiffs, output_folder):
    global zip_folder_counter  # Access the global counter variable
    zip_folder_counter = load_zip_folder_counter()  # Load the counter from the file

    # Create a unique timestamp for the output files
    epoch_time = str(int(time.time()))

    # Create a directory to store the output
    os.makedirs(output_folder, exist_ok=True)

    # Create a text file and write the text_files_data to it
    text_file_name = f"{output_folder}/cams_nom{zip_folder_counter}.txt"
    with open(text_file_name, "w") as txt_file:
        txt_file.write("\n".join(text_files_data))

    # Create a folder for TIFF files
    tiff_folder_name = f"{output_folder}/cams_nom{zip_folder_counter}"
    os.makedirs(tiff_folder_name)

    # Create a ZIP file and add TIFF files to it
    zip_file_name = f"{output_folder}/cams_nom{zip_folder_counter}.zip"
    # with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
    #     for nominee_file in nominee_files:
    #         print("path for tiffs: ", path_for_tiffs)
    #         tiff_file_name = os.path.join(
    #             path_for_tiffs, nominee_file + ".tiff")
    #         zip_file.write(os.path.join(tiff_folder_name),
    #                        arcname=os.path.basename(tiff_folder_name))
    #         print("tiff file name: ", tiff_file_name)
    #         print("zip file: ", zip_file)
    #         if os.path.exists(tiff_file_name):
    #             zip_file.write(
    #                 tiff_file_name, os.path.basename(tiff_file_name))
    #             print("zip file exist: ", zip_file)
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for nominee_file in nominee_files:
            print("path for tiffs: ", path_for_tiffs)
            tiff_file_name = os.path.join(
                path_for_tiffs, nominee_file + ".tiff")

            print("tiff file name: ", tiff_file_name)
            if os.path.exists(tiff_file_name):
                # Add the TIFF file to the folder inside the ZIP file
                zip_file.write(tiff_file_name, arcname=os.path.join(
                    os.path.basename(tiff_folder_name), os.path.basename(tiff_file_name)))
                print("tiff file added to zip: ", tiff_file_name)
            else:
                print("tiff file does not exist: ", tiff_file_name)

    zip_folder_counter += 1  # Increment the counter for the next call

    # Save the updated counter value to the file
    save_zip_folder_counter(zip_folder_counter)

    combined_zip_file_name = f"{output_folder}/combined_nom_{epoch_time}.zip"
    with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
        combined_zip_file.write(
            text_file_name, os.path.basename(text_file_name))
        combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))

    return combined_zip_file_name


def create_combined_zip_aof(nominee_files, text_files_data, path_for_tiffs, output_folder):
    global zip_folder_counter  # Access the global counter variable
    zip_folder_counter = load_zip_folder_counter()  # Load the counter from the file

    # Create a unique timestamp for the output files
    epoch_time = str(int(time.time()))

    # Create a directory to store the output
    os.makedirs(output_folder, exist_ok=True)

    # Create a text file and write the text_files_data to it
    text_file_name = f"{output_folder}/CAMS_RIA{zip_folder_counter}.txt"
    with open(text_file_name, "w") as txt_file:
        txt_file.write("\n".join(text_files_data))

    # Create a folder for TIFF files
    tiff_folder_name = f"{output_folder}/CAMS_RIA{zip_folder_counter}"
    os.makedirs(tiff_folder_name)

    # Create a ZIP file and add TIFF files to it
    zip_file_name = f"{output_folder}/CAMS_RIA{zip_folder_counter}.zip"
    # with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
    #     for nominee_file in nominee_files:
    #         print("path for tiffs: ", path_for_tiffs)
    #         tiff_file_name = os.path.join(
    #             path_for_tiffs, nominee_file + ".tiff")
    #         zip_file.write(os.path.join(tiff_folder_name),
    #                        arcname=os.path.basename(tiff_folder_name))
    #         print("tiff file name: ", tiff_file_name)
    #         print("zip file: ", zip_file)
    #         if os.path.exists(tiff_file_name):
    #             zip_file.write(
    #                 tiff_file_name, os.path.basename(tiff_file_name))
    #             print("zip file exist: ", zip_file)
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for nominee_file in nominee_files:
            print("path for tiffs: ", path_for_tiffs)
            tiff_file_name = os.path.join(
                path_for_tiffs, nominee_file + ".tiff")

            print("tiff file name: ", tiff_file_name)
            if os.path.exists(tiff_file_name):
                # Add the TIFF file to the folder inside the ZIP file
                zip_file.write(tiff_file_name, arcname=os.path.join(
                    os.path.basename(tiff_folder_name), os.path.basename(tiff_file_name)))
                print("tiff file added to zip: ", tiff_file_name)
            else:
                print("tiff file does not exist: ", tiff_file_name)

    zip_folder_counter += 1  # Increment the counter for the next call

    # Save the updated counter value to the file
    save_zip_folder_counter(zip_folder_counter)

    combined_zip_file_name = f"{output_folder}/combined_nom_{epoch_time}.zip"
    with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
        combined_zip_file.write(
            text_file_name, os.path.basename(text_file_name))
        combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))

    return combined_zip_file_name


# def create_combined_zip_aof(nominee_files, text_files_data, path_for_tiffs, output_folder):
#     # Create a unique timestamp for the output files
#     epoch_time = str(int(time.time()))

#     # Create a directory to store the output
#     os.makedirs(output_folder, exist_ok=True)

#     # Determine the text file name
#     if len(text_files_data) == 1:
#         # If there's only one text file, use the same name as the first nominee file
#         text_file_name = f"{output_folder}/{nominee_files[0]}.txt"
#     else:
#         # Otherwise, create a unique text file name
#         text_file_name = f"{output_folder}/CAMS_RIA_{epoch_time}.txt"

#     with open(text_file_name, "w") as txt_file:
#         txt_file.write("\n".join(text_files_data))

#     # Create a folder for TIFF files
#     tiff_folder_name = f"{output_folder}/CAMS_RIA"
#     os.makedirs(tiff_folder_name)

#     # Create a ZIP file and add TIFF files to it
#     zip_file_name = f"{output_folder}/CAMS_RIA_{epoch_time}.zip"
#     with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
#         for nominee_file in nominee_files:
#             tiff_file_name = os.path.join(
#                 path_for_tiffs, nominee_file + ".tiff")
#             if os.path.exists(tiff_file_name):
#                 zip_file.write(
#                     tiff_file_name, os.path.basename(tiff_file_name))

#     combined_zip_file_name = f"{output_folder}/combined_aof_{epoch_time}.zip"
#     with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
#         combined_zip_file.write(
#             text_file_name, os.path.basename(text_file_name))
#         combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))

#     os.remove(text_file_name)
#     os.remove(zip_file_name)

#     return combined_zip_file_name


current_date = dt.now()


def create_combined_zip_aof_karvy(nominee_files, dbf_data, path_for_tiffs, output_folder):
    # Create a unique timestamp for the output files
    epoch_time = str(int(time.time()))

    # Create a directory to store the output
    os.makedirs(output_folder, exist_ok=True)

    # Create a CSV file
    csv_file_name = f"{output_folder}/cams_aof_{epoch_time}.csv"

    # Write the DBF data to the CSV file, including header names

    with open(csv_file_name, "w") as csv_file:
        csv_file.write("\n".join(dbf_data))

    formatted_date = current_date.strftime("%d%m%y")

    # Convert the CSV file to a DBF file
    dbf_file_name_without = f'DOC_5874{formatted_date}'

    dbf_file_name = f"{output_folder}/{dbf_file_name_without}.dbf"

    # some_table = dbf.from_csv(csvfile=csv_file_name, filename=dbf_file_name,
    #                           field_names='FIELD1 FIELD2 FIELD3 FIELD4 FIELD5 FIELD6 FIELD7 FIELD8 FIELD9 FIELD10 FIELD11 FIELD12 FIELD13 FIELD14 FIELD15 FIELD16'.split())

    # dbf_file_name_without = 'POA'

    # dbf_file_name = f"{output_folder}/{dbf_file_name_without}.dbf"

    # some_table = dbf.from_csv(csvfile=csv_file_name, filename=dbf_file_name,
    #                           field_names='AMC_CODE ISC_CODE ISC_TRXN_N BROKER_COD FOLIO_NO CHK_DIG_NO TRXN_TYPE INVESTOR_F INVESTOR_M INVESTOR_L ADD1 ADD2 ADD3 CITY STATE COUNTRY PINCODE PHONEOFFIC PHONE_RES FAX_OFF FAX_RES EMAIL TAX_NUMBER DIV_PAYOUT PAYMENT_ME ECS_NO SCH_CODE BANK_NAME BRANCH BANK_CITY ACCT_TYPE ACCT_NO ALL_SCHEME NOM1_RELAT NOMINEE1_D NOMINATION NOMINEE1_G INVESTOR_T FHOLD_NATU REMARKS REINVEST_T NOMINEE_CO NOM1_PERCE STATUS POA_NO EFFECT_DAT EXPIRY_DAT POSTED_DAT POA_REF TITLE ADDRESS_ID PERSONAL_I POA_ISSUED DATE_OF_BI GENDER VALID_PAN UPDATE_SER POA_PEP_FL POA_OCCUPA POA_INCOME POA_NET_WO POA_NET_W2 POA_SAVING POA_SOURCE POA_SOURC2 COUNTRY_BI COUNTRY_CI COUNTRY_TA TAX_PAYER_ COUNTRY_T2 TAX_PAYER2 COUNTRY_T3 TAX_PAYER3 AADHAAR COUNTRY_OF FOLIO_LIST IMAGE_REF_ IFSC_CODE RTGS_CODE TARGET_BRO NOM2_NAME NOM2_RELAT NOM2_PERCE NOM3_NAME NOM3_RELAT NOM3_PERCE MOBILE_NO NOMINEE2_G NOMINEE3_G NOM1_MIN_F NOM2_MIN_F NOM3_MIN_F NOM2_DOB NOM3_DOB JH1_MOBILE JH2_MOBILE JH1_EMAIL_ JH2_EMAIL_ FH_MOBILE_ FH_EMAIL_I JH1_MOBIL2 JH2_MOBIL2 JH1_EMAIL2 JH2_EMAIL2 DOCUMENT_T NOM_OPT'.split())
    dbf_name = 'poa_rta_list_DBF.dbf'
    # --------------------------------------------------
    dbf_field_names = ['FIELD1', 'FIELD2', 'FIELD3', 'FIELD4', 'FIELD5', 'FIELD6', 'FIELD7',
                       'FIELD8', 'FIELD9', 'FIELD10', 'FIELD11', 'FIELD12', 'FIELD13', 'FIELD14', 'FIELD15', 'FIELD16']
    dbf_table = dbf.Table(
        filename=dbf_file_name,
        field_specs=[f"{field_name} C(50)" for field_name in dbf_field_names],
        on_disk=True,
    )
    dbf_table.open(dbf.READ_WRITE)

    # print(type(dbf_data[0]))
    # print('dbf data: ', dbf_data[0].split(','))

    for row in dbf_data:
        filtered_data = row.split(',')
        comma_separated_tuple = tuple(filtered_data)
        print("row data: ", comma_separated_tuple)
        dbf_table.append(comma_separated_tuple)
    dbf_table.close()
    # ------------------------

    # dbf_filename = 'poa_rta_list.dbf'
    # dbf_table = dbf.Table(
    #     filename=dbf_filename,
    #     field_specs=[f"{field_name} C(50)" for field_name in dbf_field_names],
    #     on_disk=True,
    # )
    # dbf_table.open(dbf.READ_WRITE)

    # data = cursor.fetchall()

    # print("data: ", data)

    # for row in data:
    #     dbf_table.append(row)

    # for row in dbf_data:
    # dbf_table.append(dbf_data.split(','))
    # for row in dbf_data:
    # Split the row by commas
    # row_values = row.split(',')

    # Ensure the number of values matches the number of fields

    # print("len row values: ", len(dbf_data))
    # print("len dbf values: ", len(dbf_field_names))
    # # if len(row_values) == len(dbf_field_names):
    # print(row)
    # dbf_table.append(row)
    # else:
    #     print(f"Skipping row: {row} as the number of values does not match the number of fields.")

    # Create a ZIP file and add TIFF files, DBF, and DBT files to it

    # Create a folder for TIFF files
    tiff_folder_name = f"{output_folder}/INP000005874{formatted_date}"
    os.makedirs(tiff_folder_name)

    zip_file_name = f"{output_folder}/INP000005874{formatted_date}.zip"
    # with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
    # for nominee_file in nominee_files:
    #     tiff_file_name = os.path.join(
    #         path_for_tiffs, nominee_file + ".tiff")
    #     if os.path.exists(tiff_file_name):
    #         zip_file.write(
    #             tiff_file_name, os.path.basename(tiff_file_name))
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for nominee_file in nominee_files:
            print("path for tiffs: ", path_for_tiffs)
            tiff_file_name = os.path.join(
                path_for_tiffs, nominee_file + ".tiff")

            print("tiff file name: ", tiff_file_name)
            if os.path.exists(tiff_file_name):
                # Add the TIFF file to the folder inside the ZIP file
                zip_file.write(tiff_file_name, arcname=os.path.join(
                    os.path.basename(tiff_folder_name), os.path.basename(tiff_file_name)))
                print("tiff file added to zip: ", tiff_file_name)
            else:
                print("tiff file does not exist: ", tiff_file_name)

    # Remove the CSV, DBF, and DBT files
    os.remove(csv_file_name)

    combined_zip_file_name = f"{output_folder}/combined_aof_{epoch_time}.zip"
    with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
        combined_zip_file.write(dbf_file_name, os.path.basename(dbf_file_name))
        combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))
        # -------------------------
        # combined_zip_file.write(f'{output_folder}/{dbf_file_name_without}.dbt',
        #                         os.path.basename(f'{output_folder}/{dbf_file_name_without}.dbt'))

    os.remove(dbf_file_name)
    # os.remove(f'{output_folder}/{dbf_file_name_without}.dbt')
    #  -------------
    return combined_zip_file_name


def create_combined_zip_karvy_nominee(nominee_files, path_for_tiffs, output_folder, custom_zip_name):
    # Create a directory to store the output
    os.makedirs(output_folder, exist_ok=True)

    tiff_folder_name = f"{output_folder}/{custom_zip_name}TRXN001"
    os.makedirs(tiff_folder_name)

    # Create a ZIP file and add TIFF files to it
    zip_file_name = f"{output_folder}/{custom_zip_name}TRXN001.zip"
    # with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
    #     for nominee_file in nominee_files:
    #         tiff_file_name = os.path.join(
    #             path_for_tiffs, nominee_file + ".tiff")
    #         if os.path.exists(tiff_file_name):
    #             zip_file.write(
    #                 tiff_file_name, os.path.basename(tiff_file_name))
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for nominee_file in nominee_files:
            print("path for tiffs: ", path_for_tiffs)
            tiff_file_name = os.path.join(
                path_for_tiffs, nominee_file + ".tiff")

            print("tiff file name: ", tiff_file_name)
            if os.path.exists(tiff_file_name):
                # Add the TIFF file to the folder inside the ZIP file
                zip_file.write(tiff_file_name, arcname=os.path.join(
                    os.path.basename(tiff_folder_name), os.path.basename(tiff_file_name)))
                print("tiff file added to zip: ", tiff_file_name)
            else:
                print("tiff file does not exist: ", tiff_file_name)

    combined_zip_file_name = f"{output_folder}/combined_{custom_zip_name}.zip"
    with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
        combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))

    # Remove the individual ZIP file
    os.remove(zip_file_name)

    return combined_zip_file_name

# def create_combined_zip_poa(nominee_files, dbf_data, path_for_tiffs, output_folder):
#     # Create a unique timestamp for the output files
#     epoch_time = str(int(time.time()))

#     # Create a directory to store the output
#     os.makedirs(output_folder, exist_ok=True)

#     # Create a CSV file
#     csv_file_name = f"{output_folder}/cams_aof_{epoch_time}.csv"

#     # Write the DBF data to the CSV file, including header names

#     with open(csv_file_name, "w") as csv_file:
#         csv_file.write("\n".join(dbf_data))

#     formatted_date = current_date.strftime("%y%m%d")

#     # Convert the CSV file to a DBF file
#     dbf_file_name_without = f'POA{formatted_date}_{epoch_time}'

#     dbf_file_name = f"{output_folder}/{dbf_file_name_without}.dbf"

#     some_table = dbf.from_csv(csvfile=csv_file_name, filename=dbf_file_name,
#                               field_names='AMC_CODE ISC_CODE ISC_TRXN FOLIO_NO TRXN_TYPE INVESTOR_F IMAGE_REF '.split())

#     # Create a ZIP file and add TIFF files, DBF, and DBT files to it
#     zip_file_name = f"{output_folder}/POA_{epoch_time}.zip"
#     with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
#         for nominee_file in nominee_files:
#             tiff_file_name = os.path.join(path_for_tiffs, nominee_file + ".tiff")
#             if os.path.exists(tiff_file_name):
#                 zip_file.write(tiff_file_name, os.path.basename(tiff_file_name))

#     # Remove the CSV, DBF, and DBT files
#     os.remove(csv_file_name)

#     combined_zip_file_name = f"{output_folder}/combined_aof_{epoch_time}.zip"
#     with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
#         combined_zip_file.write(dbf_file_name, os.path.basename(dbf_file_name))
#         combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))
#         combined_zip_file.write(f'{output_folder}/{dbf_file_name_without}.dbt',
#                                 os.path.basename(f'{output_folder}/{dbf_file_name_without}.dbt'))

#     return combined_zip_file_name


def create_combined_zip_poa(nominee_files, dbf_data, path_for_tiffs, output_folder):
    # Create a unique timestamp for the output files
    epoch_time = str(int(time.time()))

    # Create a directory to store the output
    os.makedirs(output_folder, exist_ok=True)

    # Create a directory named "poa" inside the output folder
    poa_folder = os.path.join(output_folder, "POA")
    os.makedirs(poa_folder, exist_ok=True)

    # Create a CSV file
    csv_file_name = f"{output_folder}/cams_aof_{epoch_time}.csv"

    # Write the DBF data to the CSV file, including header names
    with open(csv_file_name, "w") as csv_file:
        csv_file.write("\n".join(dbf_data))

    # formatted_date = datetime.now().strftime("%y%m%d")

    # Convert the CSV file to a DBF file
    dbf_file_name_without = 'POA'

    dbf_file_name = f"{output_folder}/{dbf_file_name_without}.dbf"

    # some_table = dbf.from_csv(csvfile=csv_file_name, filename=dbf_file_name,
    #                           field_names='AMC_CODE ISC_CODE ISC_TRXN_N BROKER_COD FOLIO_NO CHK_DIG_NO TRXN_TYPE INVESTOR_F INVESTOR_M INVESTOR_L ADD1 ADD2 ADD3 CITY STATE COUNTRY PINCODE PHONEOFFIC PHONE_RES FAX_OFF FAX_RES EMAIL TAX_NUMBER DIV_PAYOUT PAYMENT_ME ECS_NO SCH_CODE BANK_NAME BRANCH BANK_CITY ACCT_TYPE ACCT_NO ALL_SCHEME NOM1_RELAT NOMINEE1_D NOMINATION NOMINEE1_G INVESTOR_T FHOLD_NATU REMARKS REINVEST_T NOMINEE_CO NOM1_PERCE STATUS POA_NO EFFECT_DAT EXPIRY_DAT POSTED_DAT POA_REF TITLE ADDRESS_ID PERSONAL_I POA_ISSUED DATE_OF_BI GENDER VALID_PAN UPDATE_SER POA_PEP_FL POA_OCCUPA POA_INCOME POA_NET_WO POA_NET_W2 POA_SAVING POA_SOURCE POA_SOURC2 COUNTRY_BI COUNTRY_CI COUNTRY_TA TAX_PAYER_ COUNTRY_T2 TAX_PAYER2 COUNTRY_T3 TAX_PAYER3 AADHAAR COUNTRY_OF FOLIO_LIST IMAGE_REF_ IFSC_CODE RTGS_CODE TARGET_BRO NOM2_NAME NOM2_RELAT NOM2_PERCE NOM3_NAME NOM3_RELAT NOM3_PERCE MOBILE_NO NOMINEE2_G NOMINEE3_G NOM1_MIN_F NOM2_MIN_F NOM3_MIN_F NOM2_DOB NOM3_DOB JH1_MOBILE JH2_MOBILE JH1_EMAIL_ JH2_EMAIL_ FH_MOBILE_ FH_EMAIL_I JH1_MOBIL2 JH2_MOBIL2 JH1_EMAIL2 JH2_EMAIL2 DOCUMENT_T NOM_OPT'.split())
    # dbf_filename = 'poa_rta_list.dbf'
    dbf_field_names = ['AMC_CODE', 'ISC_CODE', 'ISC_TRXN_N', 'BROKER_COD', 'FOLIO_NO', 'CHK_DIG_NO', 'TRXN_TYPE', 'INVESTOR_F', 'INVESTOR_M', 'INVESTOR_L', 'ADD1', 'ADD2', 'ADD3', 'CITY', 'STATE', 'COUNTRY', 'PINCODE', 'PHONEOFFIC', 'PHONE_RES', 'FAX_OFF', 'FAX_RES', 'EMAIL', 'TAX_NUMBER', 'DIV_PAYOUT', 'PAYMENT_ME', 'ECS_NO', 'SCH_CODE', 'BANK_NAME', 'BRANCH', 'BANK_CITY', 'ACCT_TYPE', 'ACCT_NO', 'ALL_SCHEME', 'NOM1_RELAT', 'NOMINEE1_D', 'NOMINATION', 'NOMINEE1_G', 'INVESTOR_T', 'FHOLD_NATU', 'REMARKS', 'REINVEST_T', 'NOMINEE_CO', 'NOM1_PERCE', 'STATUS', 'POA_NO', 'EFFECT_DAT', 'EXPIRY_DAT', 'POSTED_DAT', 'POA_REF', 'TITLE', 'ADDRESS_ID', 'PERSONAL_I', 'POA_ISSUED', 'DATE_OF_BI', 'GENDER', 'VALID_PAN', 'UPDATE_SER', 'POA_PEP_FL', 'POA_OCCUPA', 'POA_INCOME', 'POA_NET_WO', 'POA_NET_W2', 'POA_SAVING', 'POA_SOURCE', 'POA_SOURC2', 'COUNTRY_BI', 'COUNTRY_CI', 'COUNTRY_TA', 'TAX_PAYER_', 'COUNTRY_T2', 'TAX_PAYER2', 'COUNTRY_T3', 'TAX_PAYER3', 'AADHAAR', 'COUNTRY_OF', 'FOLIO_LIST', 'IMAGE_REF_', 'IFSC_CODE', 'RTGS_CODE', 'TARGET_BRO', 'NOM2_NAME', 'NOM2_RELAT', 'NOM2_PERCE', 'NOM3_NAME', 'NOM3_RELAT', 'NOM3_PERCE', 'MOBILE_NO', 'NOMINEE2_G', 'NOMINEE3_G', 'NOM1_MIN_F', 'NOM2_MIN_F', 'NOM3_MIN_F', 'NOM2_DOB', 'NOM3_DOB', 'JH1_MOBILE', 'JH2_MOBILE', 'JH1_EMAIL_', 'JH2_EMAIL_', 'FH_MOBILE_', 'FH_EMAIL_I', 'JH1_MOBIL2', 'JH2_MOBIL2', 'JH1_EMAIL2', 'JH2_EMAIL2', 'DOCUMENT_T', 'NOM_OPT'
                       ]
    # --------------------------------------------------
    # dbf_field_names=['FIELD1' ,'FIELD2', 'FIELD3', 'FIELD4' ,'FIELD5', 'FIELD6' ,'FIELD7' ,'FIELD8', 'FIELD9' ,'FIELD10', 'FIELD11','FIELD12', 'FIELD13' ,'FIELD14' ,'FIELD15' ,'FIELD16']
    dbf_table = dbf.Table(
        filename=dbf_file_name,
        field_specs=[f"{field_name} C(50)" for field_name in dbf_field_names],
        on_disk=True,
    )
    dbf_table.open(dbf.READ_WRITE)

    for row in dbf_data:
        filtered_data = row.split(',')
        comma_separated_tuple = tuple(filtered_data)
        dbf_table.append(comma_separated_tuple)
    dbf_table.close()
    # ------------------------
    # Create a ZIP file and add TIFF files to it
    zip_file_name = f"{poa_folder}/POA.zip"
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for nominee_file in nominee_files:
            tiff_file_name = os.path.join(
                path_for_tiffs, nominee_file + ".tiff")
            if os.path.exists(tiff_file_name):
                # Store TIFF files inside the "poa" folder within the ZIP
                zip_file.write(tiff_file_name, os.path.join(
                    "POA", os.path.basename(tiff_file_name)))

    # Remove the CSV, DBF, and DBT files
    os.remove(csv_file_name)

    combined_zip_file_name = f"{output_folder}/combined_aof_{epoch_time}.zip"
    with zipfile.ZipFile(combined_zip_file_name, "w", zipfile.ZIP_DEFLATED) as combined_zip_file:
        combined_zip_file.write(dbf_file_name, os.path.basename(dbf_file_name))
        combined_zip_file.write(zip_file_name, os.path.basename(zip_file_name))
        # combined_zip_file.write(f'{output_folder}/{dbf_file_name_without}.dbt',
        # os.path.basename(f'{output_folder}/{dbf_file_name_without}.dbt'))

    return combined_zip_file_name


def load_zip_folder_counter():
    if os.path.exists("zip_folder_counter.txt"):
        with open("zip_folder_counter.txt", "r") as file:
            return int(file.read())
    else:
        return 1  # Default value if the file doesn't exist

# Function to save the counter value to a file


def save_zip_folder_counter(counter):
    with open("zip_folder_counter.txt", "w") as file:
        file.write(str(counter))

# @nominee_handler_bp.route("/quality-change", methods=["POST"])
# def set_quality_level():
#     try:
#         # Get the quality level data from the request
#         quality_level = request.json.get('qualityLevel')

#         # Update the .env file with the new quality level
#         set_key('.env', 'DPI', str(quality_level))

#         # Return a success response
#         response = {'message': 'Quality level updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         # Handle errors and return an error response
#         error_message = str(e)
#         response = {'error': error_message}
#         return jsonify(response), 500

# @nominee_handler_bp.route('/get-quality-level', methods=['GET'])
# def get_quality_level():
#     try:
#         # Get the current quality level from the .env file
#         quality_level = get_key('.env', 'DPI')

#         # Return the quality level as an integer
#         response = {'qualityLevel': int(quality_level)}
#         return jsonify(response), 200

#     except Exception as e:
#         # Handle errors and return an error response
#         error_message = str(e)
#         response = {'error': error_message}
#         return jsonify(response), 500


@nominee_handler_bp.route("/zip-size-change", methods=["POST"])
def set_zip_size():
    import psycopg2
    from src.utils.psqldb import get_connection_from_pool, psql_connect

    try:
        # Get the quality level data from the request
        zip_size = request.json.get('zipSize')
        print(zip_size)

        # Update the database with the new quality level using a raw SQL query

        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cursor = ps_connection.cursor()

        update_query = f"UPDATE tiff_config SET poa_tiff_size = {zip_size};"
        cursor.execute(update_query)
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

        # Return a success response
        response = {'message': 'Zip Size updated successfully'}
        return jsonify(response), 200

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500


@nominee_handler_bp.route('/get-zip-size', methods=['GET'])
def get_zip_size():
    from src.utils.psqldb import get_connection_from_pool, psql_connect

    try:
        # Create a connection pool and get a connection
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cursor = ps_connection.cursor()

            # Execute a SELECT query to retrieve the quality level
            select_query = "SELECT poa_tiff_size FROM tiff_config;"
            cursor.execute(select_query)

            # Fetch the quality level from the result
            zip_size = cursor.fetchone()

            if zip_size:
                # quality_level will be a tuple; extract the value
                zip_size = zip_size[0]

                # Close the cursor and the connection
                cursor.close()
                ps_connection.close()

                # Return the quality level in the response
                response = {'zipSize': zip_size}
                return jsonify(response), 200

        # If no connection is available
        return jsonify({'error': 'Database connection not available'}), 500

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500


@nominee_handler_bp.route("/quality-change", methods=["POST"])
def set_quality_level():
    from src.models.tiff_model import tiff_config_model
    from app import db
    import psycopg2
    from src.utils.psqldb import get_connection_from_pool, psql_connect

    try:
        # Get the quality level data from the request
        quality_level = request.json.get('qualityLevel')
        print(quality_level)

        # Update the database with the new quality level using a raw SQL query

        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cursor = ps_connection.cursor()

        update_query = f"UPDATE tiff_config SET poa_quality_level = {quality_level};"
        cursor.execute(update_query)
        ps_connection.commit()

        cursor.close()
        ps_connection.close()

        # Return a success response
        response = {'message': 'Quality level updated successfully'}
        return jsonify(response), 200

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500


@nominee_handler_bp.route('/get-quality-level', methods=['GET'])
def get_quality():
    from src.utils.psqldb import get_connection_from_pool, psql_connect

    try:
        # Create a connection pool and get a connection
        pool = psql_connect()
        ps_connection = get_connection_from_pool(pool)

        if ps_connection:
            # Create a cursor object to interact with the database
            cursor = ps_connection.cursor()

            # Execute a SELECT query to retrieve the quality level
            select_query = "SELECT poa_quality_level FROM tiff_config;"
            cursor.execute(select_query)

            # Fetch the quality level from the result
            quality_level = cursor.fetchone()

            if quality_level:
                # quality_level will be a tuple; extract the value
                quality_level = quality_level[0]

                # Close the cursor and the connection
                cursor.close()
                ps_connection.close()

                # Return the quality level in the response
                response = {'qualityLevel': quality_level}
                return jsonify(response), 200

        # If no connection is available
        return jsonify({'error': 'Database connection not available'}), 500

    except Exception as e:
        # Handle errors and return an error response
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500


@nominee_handler_bp.route('/generate_dbf', methods=['GET'])
def generate_dbf():
    dbf_test.fetch_data_from_database()
    return jsonify({"message": "DBF file generated successfully"})


@nominee_handler_bp.route('/download_dbf', methods=['GET'])
def download_dbf():
    return send_file('output.dbf', as_attachment=True)


@nominee_handler_bp.route('/download_excel', methods=['GET'])
def download_excel():
    return test_excel.download_excel()
