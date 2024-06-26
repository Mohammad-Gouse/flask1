from PIL import Image, ImageSequence
import os
from pdf2image import convert_from_path
from flask import make_response
import zipfile
import re
import datetime
from src.utils.data_variable import Data_Var
# Import PdfFileWriter and PdfFileReader
from PyPDF2 import PdfFileReader, PdfReader
from decouple import config

TRANSACTION_FILE_NAME = Data_Var.data_store_location
DPI = 250

print("DPI: ", DPI)


def convert_pdf_to_tiff(input_pdf_path, output_folder, dpi=DPI, max_width=1500):
    print("DPI 1: ", DPI)
    images = convert_from_path(input_pdf_path, dpi=dpi)
    print("DPIn2: ", DPI)
    # in tiff_files array append each page using for loop and decrease
    tiff_files = []
    for i, image in enumerate(images):
        tiff_path = os.path.join(output_folder, f"page_{i+1}.tiff")
        image.thumbnail((max_width, max_width * image.height //
                        image.width), Image.LANCZOS)
        image.save(tiff_path, compression="tiff_lzw")
        tiff_files.append(tiff_path)
    return tiff_files


def compress_tiff(input_path, output_path, max_width=1500):
    # Open the TIFF image
    img = Image.open(input_path)

    # Reduce the image size while preserving aspect ratio
    if img.width > max_width:
        img.thumbnail((max_width, max_width * img.height //
                      img.width), Image.LANCZOS)

    # Save the resized image with LZW compression
    img.save(output_path, compression="tiff_lzw")


def merge_tiff_files(tiff_files, output_tiff_path, max_width=1500):
    first_img = Image.open(tiff_files[0])
    # Resize the first image before appending other images
    temp_output_path = "temp.tiff"
    compress_tiff(tiff_files[0], temp_output_path, max_width=max_width)

    first_img = Image.open(temp_output_path)
    first_img.save(output_tiff_path, save_all=True, append_images=[
                   Image.open(tiff) for tiff in tiff_files[1:]])
    os.remove(temp_output_path)


# def process_single_pdf(pdf_path, output_folder):
#      os.makedirs(output_folder, exist_ok=True)
#      tiff_files = convert_pdf_to_tiff(pdf_path, output_folder)
#     return tiff_files


#     # Check if the input PDF is already a TIFF
#     if pdf_path.lower().endswith(".tiff") or pdf_path.lower().endswith(".tif"):
#         # If it's a TIFF, move it directly to the output folder
#         tiff_path = os.path.join(output_folder, os.path.basename(pdf_path))
#         os.rename(pdf_path, tiff_path)
#         return [tiff_path]
#     tiff_files = convert_pdf_to_tiff(pdf_path, output_folder)
#     return tiff_files


def process_single_pdf(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    if pdf_path.lower().endswith(".tiff") or pdf_path.lower().endswith(".tif"):
        # If it's a TIFF, extract and save its pages individually
        tiff_path = os.path.join(output_folder, os.path.basename(pdf_path))
        pages = Image.open(pdf_path)
        tiff_files = []

        for i, page in enumerate(ImageSequence.Iterator(pages)):
            page_path = os.path.join(
                output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{i+1}.tiff")
            page.save(page_path, "TIFF")
            tiff_files.append(page_path)

        return tiff_files

    tiff_files = convert_pdf_to_tiff(pdf_path, output_folder)
    return tiff_files


# def process_single_pdf(pdf_path, output_folder):
#     os.makedirs(output_folder, exist_ok=True)

#     # Check if the input PDF is already a TIFF
#     if pdf_path.lower().endswith(".tiff") or pdf_path.lower().endswith(".tif"):
#         # If it's a TIFF, move it directly to the output folder
#         tiff_path = os.path.join(output_folder, os.path.basename(pdf_path))
#         os.rename(pdf_path, tiff_path)
#         return [tiff_path]

#     tiff_files = convert_pdf_to_tiff(pdf_path, output_folder)
#     return tiff_files
# def process_single_pdf(pdf_path, output_folder):
#     os.makedirs(output_folder, exist_ok=True)

#     # Check if the input PDF is already a TIFF
#     if pdf_path.lower().endswith(".tiff") or pdf_path.lower().endswith(".tif"):
#         # If it's a TIFF, extract and save its pages individually
#         tiff_path = os.path.join(output_folder, os.path.basename(pdf_path))
#         tiff_files = []

#         pdf_document = fitz.open(pdf_path)
#         for i, page in enumerate(pdf_document):
#             page_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{i + 1}.tiff")
#             image = page.get_pil_image()
#             image.save(page_path)
#             tiff_files.append(page_path)

#         return tiff_files
#     tiff_files = convert_pdf_to_tiff(pdf_path, output_folder)
#     return tiff_files


def process_multiple_pdfs(pdf_files, overall_output_folder, file_name):
    os.makedirs(overall_output_folder, exist_ok=True)
    tiff_files_list = []

    for pdf_file in pdf_files:
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
        output_folder = os.path.join(overall_output_folder, pdf_name)
        print("output folder: ", output_folder)
        # Create folder for each input PDF
        os.makedirs(output_folder, exist_ok=True)
        tiff_files = process_single_pdf(pdf_file, output_folder)
        # Append all generated TIFF files to the list
        tiff_files_list.extend(tiff_files)

    # Merge all TIFF files into a single final TIFF file
    final_tiff_path = os.path.join(overall_output_folder, f"{file_name}.tiff")
    print(final_tiff_path)
    merge_tiff_files(tiff_files_list, final_tiff_path)

    for pdf_file in pdf_files:
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
        output_folder = os.path.join(overall_output_folder, pdf_name)
        for root, dirs, files in os.walk(output_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            os.rmdir(root)
    tiff_file_size = os.path.getsize(final_tiff_path)
    return final_tiff_path, tiff_file_size
