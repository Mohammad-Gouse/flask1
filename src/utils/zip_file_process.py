import os
import zipfile

max_file_size_in_mb = 4


def get_current_zip_file_size(zip_file_path):
    # Get the current ZIP file size in bytes
    if os.path.exists(zip_file_path):
        zip_file_size = os.path.getsize(zip_file_path)
        return zip_file_size
    return 0


def create_new_zip_folder(zip_prefix):
    # Append the folder counter to the folder name
    global zip_folder_counter
    new_zip_folder_name = f"{zip_prefix}/{zip_folder_counter}"
    zip_folder_counter += 1
    return new_zip_folder_name


def add_tiff_to_zip(tiff_files, file_name, zip_file_path, zip_folder_name):
    try:
        # Get the current ZIP file size
        current_zip_file_size = get_current_zip_file_size(zip_file_path)

        # Calculate the total size (current ZIP size + new TIFF files)
        total_zip_size_mb = current_zip_file_size / \
            (1024 * 1024) + sum(os.path.getsize(tiff) / (1024 * 1024)
                                for tiff in tiff_files)

        # Check if adding new TIFF files will exceed the limit
        if total_zip_size_mb > max_file_size_in_mb:
            # Create a new ZIP file if the total size exceeds the limit
            current_zip_file_size = 0  # Reset current ZIP file size to 0
            return create_new_zip_folder(zip_folder_name)

        # Create the ZIP folder or directories if they don't exist
        os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

        temp_dir = "temp_tiff_files"
        os.makedirs(temp_dir, exist_ok=True)

        file_name = f"{file_name}.tiff"

        for i, file in enumerate(tiff_files):
            temp_file_path = os.path.join(temp_dir, f"temp_tiff_{i}.tiff")
            base_filename = os.path.basename(file)
            os.rename(file, temp_file_path)

        # Add the temporary TIFF files to the ZIP folder
        with zipfile.ZipFile(zip_file_path, 'a') as zip_file:
            folder_name_inside_zip = f'{zip_folder_name}'
            for i, file in enumerate(tiff_files):
                file_name_in_zip = os.path.join(
                    folder_name_inside_zip, f"TIFF-{file_name}")
                zip_file.write(os.path.join(
                    temp_dir, f"temp_tiff_{i}.tiff"), file_name_in_zip)

        # Remove the temporary TIFF files and directory
        for i, file in enumerate(tiff_files):
            temp_file_path = os.path.join(temp_dir, f"temp_tiff_{i}.tiff")
            os.remove(temp_file_path)
        os.rmdir(temp_dir)

        print("TIFF file added to the ZIP folder successfully.")
        return zip_folder_name

    except zipfile.BadZipFile:
        pass
    except Exception as e:
        pass


def delete_temporary_folder(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(folder_path)
        print(f"Temporary folder '{folder_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the temporary folder: {e}")
