import os
import re
import datetime
import zipfile
from flask import Flask, request, jsonify,make_response
from src.utils import pdf_to_tiff_nominee
from src.utils.data_variable import Data_Var
from src.api.nominee import nominee_handler

TRANSACTION_FILE_NAME = Data_Var.data_store_location

max_file_size_in_bytes = 4 * 1024 * 1024
zip_folder_counter=1

# def add_tiff_to_zip(tiff_data_list, file_name, paths):
#     try:
#         temp_dir = "temp_tiff_files"
#         os.makedirs(temp_dir, exist_ok=True)

#         # Save the TIFF data to temporary files
#         for i, tiff_data in enumerate(tiff_data_list):
#             temp_file_path = os.path.join(temp_dir, f"temp_tiff_{i}.tiff")
#             with open(temp_file_path, "wb") as temp_tiff_file:
#                 temp_tiff_file.write(tiff_data)

#         # Add the temporary TIFF files to the ZIP folder
#         with zipfile.ZipFile(paths, 'a') as zip_file:
#             folder_name_inside_zip = os.path.basename(paths)
#             for i, tiff_data in enumerate(tiff_data_list):
#                 file_name_in_zip = os.path.join(
#                     folder_name_inside_zip, f"{file_name}tiff{i}.tiff")
#                 with open(os.path.join(temp_dir, f"temp_tiff_{i}.tiff"), "rb") as temp_tiff_file:
#                     zip_file.writestr(file_name_in_zip, temp_tiff_file.read())

#         # Remove the temporary TIFF files and directory
#         for i, tiff_data in enumerate(tiff_data_list):
#             temp_file_path = os.path.join(temp_dir, f"temp_tiff_{i}.tiff")
#             os.remove(temp_file_path)
#         os.rmdir(temp_dir)

#         print("TIFF file added to the ZIP folder successfully.")
#         return paths
#     except zipfile.BadZipFile:
#         print("Invalid zip file.")
#     except Exception as e:
#         print(f"An error occurred: {e}")




# def add_tiff_to_zip_api(tiff_data_list, file_name):
#     try:
#         global zip_folder_counter
#         main_folder_name = "aof"
#         folder_year = datetime.datetime.now().strftime("%Y")
#         folder_month = nominee_handler.get_month_name(int(datetime.datetime.now().strftime("%m")))
#         folder_day = datetime.datetime.now().strftime("%d")
#         sub_folder_name = f'cams/{folder_year}/{folder_month}/{folder_day}'
#         # year=datetime.now().strftime("%Y")
#         # month=datetime.now().strftime("%b")
#         # date=datetime.datetime.now().date()
#         #  Calculate the total size of all TIFF files in the tiff_data_list
#         total_size_of_tiff_data = sum(len(tiff_data) for tiff_data in tiff_data_list)
#         # kb_uploaded_tiff = len(tiff_data_list) / 1024
#         # mb_uploaded_tiff = kb_uploaded_tiff / 1024
#         print("total_size_of_tiff_data", total_size_of_tiff_data)

#         current_zip_file_path = get_current_zip_file_size(TRANSACTION_FILE_NAME)
#         print(current_zip_file_path)
#         # Calculate the total size of TIFF and ZIP data
#         total_size_of_tiff_and_zip =   current_zip_file_path+total_size_of_tiff_data
#         print(total_size_of_tiff_and_zip)
#         if total_size_of_tiff_and_zip >= max_file_size_in_bytes:
#             print("if statement is executed")
#             zip_folder_counter = zip_folder_counter + 1
#             print(zip_folder_counter)
#             new_file_name = get_file_name(main_folder_name, sub_folder_name)
#             zip_path = f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{new_file_name}.zip'
#             path = add_tiff_to_zip(tiff_data_list, new_file_name, zip_path)
#             return ({"message": "TIFF file added to the ZIP folder successfully.", "zip_folder_name": os.path.basename(path)}), 200
#         else:
#             print("else statement is executed")
#             file_name = get_file_name(main_folder_name, sub_folder_name)
#             current_zip_file_path = add_tiff_to_zip(
#                 tiff_data_list, file_name, f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}/{file_name}.zip')
#             return ({"message": "TIFF file added to the ZIP folder successfully.", "zip_folder_name": os.path.basename(current_zip_file_path)}), 200

#     except Exception as e:
#         return jsonify({"message": f"An error occurred: {e}"}), 500


# def get_file_name(main, sub_folder):
#     global zip_folder_counter
#     main_folder_name = main
#     sub_folder_name = sub_folder
#     # year=datetime.now().strftime("%Y")
#     # month=datetime.now().strftime("%b")
#     # date=datetime.datetime.now().date()
#     # Get the current date in the format "DDMMYYYY"
#     current_date = datetime.datetime.now().strftime("%d%m%Y")
#     is_exist = os.path.exists(f'{TRANSACTION_FILE_NAME}')
#     if not is_exist:
#         # Create a new directory because it does not exist
#         os.makedirs(f'{TRANSACTION_FILE_NAME}')
#     is_main_folder_exist = os.path.exists(
#         f'{TRANSACTION_FILE_NAME}/{main_folder_name}')
#     if not is_main_folder_exist:
#         # Create a new directory because it does not exist
#         os.makedirs(f'{TRANSACTION_FILE_NAME}/{main_folder_name}')
#     is_sub_older_Exist = os.path.exists(
#         f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')
#     if not is_sub_older_Exist:
#         # Create a new directory because it does not exist
#         os.makedirs(
#             f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')
  
#     files_in_directory = os.listdir(
#         f'{TRANSACTION_FILE_NAME}/{main_folder_name}/{sub_folder_name}')
#     # Use a regular expression to extract the numeric suffix from the filenames
#     suffixes = [int(re.search(r"\d+$", file_name).group())
#                 for file_name in files_in_directory if re.match(r"CAMNOM\d{8}_\d+$", file_name)]
    
#     print("Current files_in_directory:", files_in_directory)
#     print("Current suffixes:", suffixes)

   
#     file_name = f"AOF_CAMS_{current_date}_{zip_folder_counter}"
#     print(zip_folder_counter)
#     return file_name



# def get_current_zip_file_size(target_directory):
#     # Get the current ZIP file size in bytes
#     try:
#         latest_zip_file_path = get_current_zip_file(target_directory)
#         if latest_zip_file_path:
#             total_size = os.path.getsize(latest_zip_file_path)
#             return total_size
#         else:
#             return 0
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return 0

# def get_current_zip_file(target_directory):
#     try:
#         latest_zip_file_path = None
#         latest_modification_time = 0

#         for root, _, files in os.walk(target_directory):
#             for file in files:
#                 if file.endswith('.zip'):
#                     file_path = os.path.join(root, file)
#                     modification_time = os.path.getmtime(file_path)
#                     if modification_time > latest_modification_time:
#                         latest_modification_time = modification_time
#                         latest_zip_file_path = file_path

#         return latest_zip_file_path
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None



# def convert_tiff_to_zip(tiff_path, pdf_file_name):
#     global zip_folder_counter
#     zip_path = f'{TRANSACTION_FILE_NAME}/aof/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}'
#     tiff_filename = os.path.basename(tiff_path)
#     tiff_file_size=get_tiff_file_size(tiff_path)
#     print(tiff_file_size)
#     current_zip_file_path = get_zip_file_size(TRANSACTION_FILE_NAME)
#     print(current_zip_file_path)
#     total_size=current_zip_file_path+tiff_file_size
#     print(total_size)
#     if total_size>max_file_size_in_bytes:
#        new_zip_file_name=new_zip_file_names(pdf_file_name)
#        print(new_zip_file_name)
#        zip_file_path=f'{TRANSACTION_FILE_NAME}/aof/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/{new_zip_file_name}'
#        print("123")
#        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#             zip_file.write(tiff_path, arcname=tiff_filename)
#             print(f"TIFF file '{tiff_filename}' converted to ZIP file '{zip_file_path}'.")
#             os.remove(tiff_path)
#             return ({"message":"tiff file converted into zip file "})
#     else:
#         # file_name=current_zip_file_name(pdf_file_name)
#         # print(file_name)
#         zip_file_paths=f'{TRANSACTION_FILE_NAME}/aof/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/{pdf_file_name}.zip'
#         print("245")
#         with zipfile.ZipFile(zip_file_paths, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#             zip_file.write(tiff_path, arcname=tiff_filename)
#             print(f"TIFF file '{tiff_filename}' converted to ZIP file '{zip_file_paths}'.")
#             os.remove(tiff_path)

#             return ({"message":"tiff file converted into zip file "})

# def convert_tiff_to_zip(tiff_path, pdf_file_name):
#     global zip_folder_counter
#     zip_path = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}'
#     tiff_filename = os.path.basename(tiff_path)
#     tiff_file_size = get_tiff_file_size(tiff_path)
#     print(tiff_file_size)
#     current_zip_file_size = get_zip_file_size(TRANSACTION_FILE_NAME)
#     print(current_zip_file_size)
#     total_size = current_zip_file_size + tiff_file_size
#     print(total_size)
    
#     if total_size > max_file_size_in_bytes:
#         new_zip_file_name = new_zip_file_names(pdf_file_name)
#         print(new_zip_file_name)
#         zip_file_path = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/{new_zip_file_name}.zip'  # Change the format here
#         print("123")
        
#         # Check if total_size is greater than 4MB
#         if total_size > 4 * 1024 * 1024:  # 4MB in bytes
#             # Create a new folder "CAMS_RTA" and save the zip file there
#             cams_rta_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_RTA'
#             os.makedirs(cams_rta_folder, exist_ok=True)
#             new_zip_file_path = os.path.join(cams_rta_folder, os.path.basename(zip_file_path))
#             with zipfile.ZipFile(new_zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 zip_file.write(tiff_path, arcname=tiff_filename)
#                 print(f"TIFF file '{tiff_filename}' converted to ZIP file '{new_zip_file_path}'.")
#                 os.remove(tiff_path)
#         else:
#             with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 zip_file.write(tiff_path, arcname=tiff_filename)
#                 print(f"TIFF file '{tiff_filename}' converted to ZIP file '{zip_file_path}'.")
#                 os.remove(tiff_path)
        
#         return {"message": "tiff file converted into zip file "}
    
#     else:
#         # file_name = current_zip_file_name(pdf_file_name)
#         # print(file_name)
#         zip_file_paths = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_RTA_{pdf_file_name}.zip'  # Change the format here
#         print("245")
        
#         # Check if total_size is greater than 4MB
#         if total_size > 4 * 1024 * 1024:  # 4MB in bytes
#             # Create a new folder "CAMS_RTA" and save the zip file there
#             cams_rta_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_RTA'
#             os.makedirs(cams_rta_folder, exist_ok=True)
#             new_zip_file_path = os.path.join(cams_rta_folder, os.path.basename(zip_file_paths))
#             with zipfile.ZipFile(new_zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 zip_file.write(tiff_path, arcname=tiff_filename)
#                 print(f"TIFF file '{tiff_filename}' converted to ZIP file '{new_zip_file_path}'.")
#                 os.remove(tiff_path)
#         else:
#             with zipfile.ZipFile(zip_file_paths, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 zip_file.write(tiff_path, arcname=tiff_filename)
#                 print(f"TIFF file '{tiff_filename}' converted to ZIP file '{zip_file_paths}'.")
#                 os.remove(tiff_path)
        
#         return {"message": "tiff file converted into zip file "}
# def get_tiff_file_size(tiff_file_path):
#     try:
#         file_size = os.path.getsize(tiff_file_path)
#         return file_size
#     except FileNotFoundError:
#         print(f"File '{tiff_file_path}' not found.")
#         return None
    
# def get_zip_file_size(zip_path):    
#     zip_files = [file for file in os.listdir(zip_path) if file.endswith(".zip")]
#     if not zip_files:
#         return 0  # Return 0 if no zip files are present
#     zip_files.sort(key=lambda x: os.path.getmtime(os.path.join(zip_path, x)))
#     latest_zip = zip_files[-1]

#     # Get the size of the latest ZIP file
#     latest_zip_path = os.path.join(zip_path, latest_zip)
#     zip_size = os.path.getsize(latest_zip_path)
#     return zip_size

# def current_zip_file_name(file_name):
#     file_name = f'{TRANSACTION_FILE_NAME}/aof/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_RIA_{file_name}.zip'
#     return file_name

# def new_zip_file_names(file_name):
#     global zip_folder_counter
#     zip_folder_counter=zip_folder_counter+1
#     new_file_name = f'{TRANSACTION_FILE_NAME}/aof/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_RIA_{file_name}_{zip_folder_counter}.zip'
#     return new_file_name




def get_tiff_file_size(tiff_file_path):
    try:
        file_size = os.path.getsize(tiff_file_path)
        return file_size
    except FileNotFoundError:
        print(f"File '{tiff_file_path}' not found.")
        return None
    
def get_zip_file_size(zip_path):    
    zip_files = [file for file in os.listdir(zip_path) if file.endswith(".zip")]
    if not zip_files:
        return 0  # Return 0 if no zip files are present
    zip_files.sort(key=lambda x: os.path.getmtime(os.path.join(zip_path, x)))
    latest_zip = zip_files[-1]

    # Get the size of the latest ZIP file
    latest_zip_path = os.path.join(zip_path, latest_zip)
    zip_size = os.path.getsize(latest_zip_path)
    return zip_size

# def current_zip_file_name(file_name):
#     file_name = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_NOM_{zip_folder_counter}.zip'
#     return file_name






# def convert_tiff_to_zip(tiff_path):
#     global zip_folder_counter
#     zip_path = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_NOM_{zip_folder_counter}'
#     # main_folder="nominee"
#     # sub_folder=f'cams/{datetime.datetime.now().strftime("%Y/%B/%d")}'
#     tiff_filename = os.path.basename(tiff_path)
#     tiff_file_size = get_tiff_file_size(tiff_path)
#     print(tiff_file_size)
#     current_zip_file_size = get_zip_file_size(zip_path)
#     print(current_zip_file_size)
#     total_size = current_zip_file_size + tiff_file_size
#     print(total_size) 

#     if total_size >= max_file_size_in_bytes:
#         zip_folder_counter=zip_folder_counter+1
#         new_zip_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_NOM_{zip_folder_counter}' # Increment the counter
#         os.makedirs(new_zip_folder, exist_ok=True)
#         new_zip_file_path = os.path.join(new_zip_folder, f'CAMS_NOM_{zip_folder_counter}.zip')
#         result=zip_file_conversion(new_zip_file_path,tiff_path,tiff_filename)
#         return ({"message":"zip file converted successfully"})
#     else:
#         new_zip_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/{datetime.datetime.now().strftime("%Y/%B/%d")}/CAMS_NOM_{zip_folder_counter}'
#         os.makedirs(new_zip_folder, exist_ok=True)
#         new_zip_file_path = os.path.join(new_zip_folder, f'CAMS_NOM_{zip_folder_counter}.zip')
#         result=zip_file_conversion(new_zip_file_path,tiff_path,tiff_filename)
#         return ({"message":"zip file converted successfully"})





# def zip_file_conversion(new_zip_file_path,tiff_path,tiff_filename):
#     with zipfile.ZipFile(new_zip_file_path, 'a', zipfile.ZIP_DEFLATED) as zip_file:
#         zip_file.write(tiff_path, arcname=tiff_filename)
#         print(f"TIFF file '{tiff_filename}' converted to ZIP file '{new_zip_file_path}'.")
#         os.remove(tiff_path)
#         return {"message": "Tiff file successfully converted into zip file"}



def convert_tiff_to_zip(tiff_path, pdf_file_name):
    zip_folder = f'{TRANSACTION_FILE_NAME}/nominee/cams/'

    tiff_filename = os.path.basename(tiff_path)
    zip_filename = f'CAMS_NOM_{pdf_file_name}.zip'
    zip_path = os.path.join(zip_folder, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(tiff_path, arcname=tiff_filename)
    
    print(f"TIFF file '{tiff_filename}' converted to ZIP file '{zip_path}'.")
    
    os.remove(tiff_path)
    
    return zip_path,tiff_filename
