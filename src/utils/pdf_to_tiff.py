from PIL import Image
import os
from pdf2image import convert_from_path
from src.utils.data_variable import Data_Var
import logging

PDF_TO_TIFF=Data_Var.data_store_location

logging.basicConfig(level=logging.WARNING)

def convert_pdf_to_tiff(input_pdf_path, output_folder, dpi=250, max_width=1000):
    logging.getLogger("pdf2image").setLevel(logging.ERROR)
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.ERROR)
    logging.getLogger("TiffImagePlugin").setLevel(logging.ERROR)
    images = convert_from_path(input_pdf_path, dpi=dpi)
    # in tiff_files array append each page using for loop and decrease
    tiff_files = []
    for i, image in enumerate(images):
        tiff_path = os.path.join(output_folder, f"page_{i+1}.tiff")
        image.thumbnail((max_width, max_width * image.height //
                        image.width), Image.LANCZOS)
        image.save(tiff_path, compression="tiff_lzw")
        tiff_files.append(tiff_path)
        logging.getLogger().setLevel(logging.WARNING)

    return tiff_files


def compress_tiff(input_path, output_path, max_width=1000):
    # Open the TIFF image
    img = Image.open(input_path)

    # Reduce the image size while preserving aspect ratio
    if img.width > max_width:
        img.thumbnail((max_width, max_width * img.height //
                      img.width), Image.LANCZOS)

    # Save the resized image with LZW compression
    img.save(output_path, compression="tiff_lzw")


def merge_tiff_files(tiff_files, output_tiff_path, max_width=1000):
    first_img = Image.open(tiff_files[0])
    # Resize the first image before appending other images
    temp_output_path = "temp.tiff"
    compress_tiff(tiff_files[0], temp_output_path, max_width=max_width)

    first_img = Image.open(temp_output_path)
    first_img.save(output_tiff_path, save_all=True, append_images=[
                   Image.open(tiff) for tiff in tiff_files[1:]])
    os.remove(temp_output_path)


def process_single_pdf(pdf_path):
    output_folder = "tiff_output"
    os.makedirs(output_folder, exist_ok=True)
    convert_pdf_to_tiff(pdf_path, output_folder)
    tiff_files = [os.path.join(output_folder, f)
                  for f in os.listdir(output_folder)]
    return tiff_files


def process_multiple_pdfs(pdf_files):
    tiff_files_list = []
    for pdf_file in pdf_files:
        tiff_files = process_single_pdf(pdf_file)
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]

        output_tiff_path = f"{pdf_name}.tiff"
        merge_tiff_files(tiff_files, output_tiff_path)
        tiff_files_list.append(output_tiff_path)

        # Delete tiff files from tiff_output folder
        tiff_output_dir = "tiff_output"
        for file_name in os.listdir(tiff_output_dir):
            file_path = os.path.join(tiff_output_dir, file_name)
            os.remove(file_path)
        os.rmdir(tiff_output_dir)

    return tiff_files_list
