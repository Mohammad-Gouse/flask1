# import fitz  # PyMuPDF
# from PIL import Image

# # def is_color_pdf(pdf_path):
# #     # Open the PDF file
# #     pdf_document = fitz.open(pdf_path)

# #     # Initialize counters for color and grayscale pages
# #     color_pages = 0
# #     grayscale_pages = 0

# #     # Iterate through each page in the PDF
# #     for page_number in range(pdf_document.page_count):
# #         page = pdf_document.load_page(page_number)
# #         pix = page.get_pixmap()

# #         # Check whether the page contains color or grayscale
# #         print("pix.n: ", pix.n)
# #         print("pix.alpha: ", pix.alpha)
# #         if pix.n - pix.alpha < 4:
# #             grayscale_pages += 1
# #         else:
# #             color_pages += 1

# #     # Close the PDF document
# #     # pdf_document.close()

# #     print("colorpages: ", color_pages)
# #     print("black and white: ", grayscale_pages)

# #     # Determine if the PDF is color or black and white
# #     if color_pages > 0:
# #         return "Color PDF"
# #     elif grayscale_pages == pdf_document.page_count:
# #         return "Black and White PDF"
# #     else:
# #         return "Mixed Color and Black and White PDF"


# import fitz  # PyMuPDF

# def convert_pdf_to_bw(input_pdf, output_pdf):
#     doc = fitz.open(input_pdf)
#     pdf_bytes = b""

#     for page_number in range(len(doc)):
#         page = doc[page_number]
#         image_list = page.get_pixmap_list()

#         for image in image_list:
#             xref = image[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]

#             # Convert the image to grayscale
#             # This assumes you're working with RGB images
#             # If you have CMYK images, you may need to adjust the conversion method
#             gray_image = fitz.Pixmap(fitz.csGRAY, image_bytes, image.width, image.height)

#             # Replace the original image with the grayscale one
#             page.show_pixmap(xref, gray_image)

#     doc.save(output_pdf)
#     doc.close()

# input_pdf = "C:/Users/ASUS/Downloads/iifl_assets/Dhaval_PMS_POA.pdf"
# output_pdf = "C:/Users/ASUS/Downloads/iifl_assets/"
# convert_pdf_to_bw(input_pdf, output_pdf)


# import PyPDF2

# # Define the input and output file paths
# input_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_AOF.pdf"

# # "C:\Users\ASUS\Downloads\DHAVAL FAMILY PRIVATE TRUST\DHAVAL FAMILY PRIVATE TRUST\Dhaval_AOF.pdf"
# output_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_AOF.pdf"

# # Open the input PDF and create an output PDF
# with open(input_pdf_path, 'r') as input_pdf_file, open(output_pdf_path, 'w') as output_pdf_file:
#     pdf_reader = PyPDF2.PdfFileReader(input_pdf_file)
#     pdf_writer = PyPDF2.PdfFileWriter()

#     # Iterate through the pages of the input PDF
#     for page_num in range(pdf_reader.numPages):
#         page = pdf_reader.getPage(page_num)

#         # Convert the page to grayscale
#         page = page.getContents()
#         page.encode('jpeg', resolution=300, options={'color': 0})
#         pdf_writer.addPage(page)

#     # Write the grayscale pages to the output PDF
#     pdf_writer.write(output_pdf_file)


# import os

# path = r"C:/Users/ASUS/Downloads/iifl_assets/Dhaval_PMS_POA.pdf"
# assert os.path.isfile(path)
# with open(path, "r") as f:
#     print("opening...")
#     pass


# import PyPDF2

# # Define the input and output file paths
# input_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_WL.pdf"

# # "C:\Users\ASUS\Downloads\DHAVAL FAMILY PRIVATE TRUST\DHAVAL FAMILY PRIVATE TRUST\Dhaval_AOF.pdf"
# output_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/sample.pdf"


# # Open the input PDF and create an output PDF
# with open(input_pdf_path, 'rb') as input_pdf_file, open(output_pdf_path, 'wb') as output_pdf_file:
#     print("in fi: ",input_pdf_file)
#     pdf_reader = PyPDF2.PdfReader(input_pdf_file)
#     pdf_writer = PyPDF2.PdfFileWriter()

#     # Iterate through the pages of the input PDF
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]

#         # Convert the page to grayscale
#         page.encode('jpeg', resolution=300, options={'color': 0})
#         pdf_writer.add_page(page)

#     # Write the grayscale pages to the output PDF
#     pdf_writer.write(output_pdf_file)


# import PyPDF2

# # Define the input and output file paths
# input_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_WL.pdf"
# output_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/test1.pdf"

# # Open the input PDF and create an output PDF
# with open(input_pdf_path, 'rb') as input_pdf_file, open(output_pdf_path, 'wb') as output_pdf_file:
#     pdf_reader = PyPDF2.PdfReader(input_pdf_file)
#     pdf_writer = PyPDF2.PdfWriter()

#     # Iterate through the pages of the input PDF
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]

#         # Convert the page to grayscale
#         page.encode('jpeg', resolution=300, options={'color': 0})
#         pdf_writer.add_page(page)

#     # Write the grayscale pages to the output PDF
#     pdf_writer.write(output_pdf_file)


# import PyPDF2
# from PIL import Image

# # Define the input and output file paths
# input_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_WL.pdf"
# output_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/test1.pdf"


# # Open the input PDF and create an output PDF
# with open(input_pdf_path, 'rb') as input_pdf_file, open(output_pdf_path, 'wb') as output_pdf_file:
#     pdf_reader = PyPDF2.PdfReader(input_pdf_file)
#     pdf_writer = PyPDF2.PdfWriter()

#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]

#         # Convert the page to grayscale using Pillow (PIL)
#         img = page.get_page_imageno(page_num)
#         img = img.convert('L')  # Convert to grayscale

#         # Create a new page with the grayscale image
#         new_page = pdf_writer.add_page()
#         new_page.mergeTranslatedPage(page, 0, 0)  # Preserve the original page size

#         # Draw the grayscale image on the new page
#         x, y, w, h = page.trimbox
#         new_page.addImage(img, x, y, w, h)

#     # Write the grayscale pages to the output PDF
#     pdf_writer.write(output_pdf_file)

# import PyPDF2
# from PIL import Image

# # Define the input and output file paths
# input_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_WL.pdf"
# output_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/test1.pdf"


# # Open the input PDF and create an output PDF
# with open(input_pdf_path, 'rb') as input_pdf_file, open(output_pdf_path, 'wb') as output_pdf_file:
#     pdf_reader = PyPDF2.PdfReader(input_pdf_file)
#     pdf_writer = PyPDF2.PdfWriter()

#     for page_num in range(pdf_reader.numPages):
#         page = pdf_reader.getPage(page_num)

#         # Convert the page to a grayscale image
#         img = page.createXObject()
#         img = img.convert('L')  # Convert to grayscale

#         # Create a new page with the grayscale image
#         new_page = pdf_writer.addBlankPage(page.mediaBox.getWidth(), page.mediaBox.getHeight())
#         new_page.mergeTranslatedPage(page)
#         new_page.addXObject(img, 0, 0)

#     # Write the grayscale pages to the output PDF
#     pdf_writer.write(output_pdf_file)

# import fitz  # PyMuPDF
# import os

# # Define input and output file paths

# input_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_WL.pdf"
# output_pdf_path = "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/test1.pdf"


# # Function to convert a page to grayscale
# def convert_page_to_grayscale(page):
#     pix = page.get_pixmap()
#     pix = pix.convert_to_grayscale()
#     page.insert_image(page.rect, pixmap=pix)

# # Create a new PDF with grayscale pages
# output_pdf = fitz.open()
# input_pdf = fitz.open(input_pdf_path)

# for page_num in range(len(input_pdf)):
#     page = input_pdf.load_page(page_num)
#     media_box = page.mediabox
#     output_page = output_pdf.new_page(width=media_box.width, height=media_box.height)
#     output_page.show_pdf_page(page)
#     convert_page_to_grayscale(output_page)

# # Save the output PDF
# output_pdf.save(output_pdf_path)
# output_pdf.close()
# input_pdf.close()

# print(f"Conversion complete. Output PDF saved to '{output_pdf_path}'")


# from os.path import join
import os
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path  # https://pypi.org/project/pdf2image/
from img2pdf import convert  # https://pypi.org/project/img2pdf/
from os.path import join, dirname, basename


# def convertBlack(inputpath, outputpath):
#     with TemporaryDirectory() as temp_dir:  # Saves images temporarily in disk rather than RAM to speed up parsing
#         # Converting pages to images
#         print("Parsing pages to grayscale images. This may take a while")
#         images = convert_from_path(
#             inputpath,
#             output_folder=outputpath,
#             grayscale=True,
#             fmt="jpeg",
#             thread_count=4
#         )

#         print("outputfolder: ", outputpath)

#         image_list = list()
#         for page_number in range(1, len(images) + 1):
#             path = join(temp_dir, "page_" + str(page_number) + ".jpeg")
#             image_list.append(path)
#             # (page_number - 1) because index starts from 0
#             images[page_number-1].save(path, "JPEG")

#         with open("Gray_PDF.pdf", "bw") as gray_pdf:
#             gray_pdf.write(convert(image_list))

#         print("The new page is saved as Gray_PDF.pdf in the current directory.")

def convertBlack(inputpath, outputpath):
    # output_dir = dirname(inputpath)  # Get the directory of the input PDF
    # Create the output PDF file path

    print("outputpath: ", outputpath)
    # output_dir = "C:/Users/ASUS/Documents/coursera/testing"
    output_dir = f"C:/Users/ASUS/Documents/iifl_demo_testing/mf-utility-be/data/temp_folder_FN$L$IFFWPMS$810"

    # "C:/Users/ASUS/Documents/coursera/testing"

    print("output_dir: ", output_dir)
    output_file = join(output_dir, basename(inputpath))
    print("output_file: ", output_file)

    with TemporaryDirectory() as temp_dir:
        print("Parsing pages to grayscale images. This may take a while")
        images = convert_from_path(
            inputpath,
            output_folder=temp_dir,
            grayscale=True,
            fmt="jpeg",
            thread_count=4
        )

        image_list = list()
        for page_number in range(1, len(images) + 1):
            path = join(temp_dir, "page_" + str(page_number) + ".jpeg")
            image_list.append(path)
            images[page_number-1].save(path, "JPEG")

        with open(output_file, "wb") as gray_pdf:
            gray_pdf.write(convert(image_list))

        print(
            f"The new PDF is saved as {basename(output_file)} in the same directory as the input PDF.")


with TemporaryDirectory() as temp_dir:  # Saves images temporarily in disk rather than RAM to speed up parsing
    # Converting pages to images
    print("Parsing pages to grayscale images. This may take a while")
    images = convert_from_path(
        "C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_PMS POA.pdf",
        output_folder=temp_dir,
        grayscale=True,
        fmt="jpeg",
        thread_count=4
    )

    print("outputfolder: ", temp_dir)

    image_list = list()
    for page_number in range(1, len(images) + 1):
        path = join(temp_dir, "page_" + str(page_number) + ".jpeg")
        image_list.append(path)
        # (page_number - 1) because index starts from 0
        images[page_number-1].save(path, "JPEG")

    with open("Gray_PDF.pdf", "bw") as gray_pdf:
        gray_pdf.write(convert(image_list))

    print("The new page is saved as Gray_PDF.pdf in the current directory.")
