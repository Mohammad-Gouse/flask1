# import pdf2image
# import numpy as np

# images = convert_from_path('C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_WL.pdf')
# sw=0
# color=0
# for image in images:
#     img = np.array(image.convert('HSV'))
#     hsv_sum = img.sum(0).sum(0)
#     if hsv_sum[0] == 0 and hsv_sum[1] == 0:
#         sw += 1
#     else:
#         color += 1

# from pdf2image import convert_from_path
# import numpy as np

# # Replace the path with the correct PDF file path
# pdf_path = 'C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/500_stamp.pdf'

# images = convert_from_path(pdf_path)

# sw = 0
# color = 0

# for image in images:
#     # Convert the PIL image to a NumPy array
#     img = np.array(image)
#     print("img: ", img)
#     print("img.shape: ", img.shape[-1])
#     if img.shape[-1] == 3:
#         # If the image has 3 channels (RGB), consider it in color
#         color += 1
#     else:
#         # If the image has only 1 channel, consider it black and white
#         sw += 1

# print(f"Color images: {color}")
# print(f"Black and white images: {sw}")

# from pdf2image import convert_from_path
# import numpy as np

# # Replace the path with the correct PDF file path
# pdf_path = 'C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/hi this is pdf sample.pdf'

# images = convert_from_path(pdf_path)

# sw = 0
# color = 0

# for image in images:
#     # Convert the PIL image to a NumPy array
#     img = np.array(image)
#     # print(len(img.shape))
#     print(img.shape)
#     if len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[-1] == 1):
#         # If the image is grayscale (single channel) or has 3 channels with identical values, consider it black and white
#         sw += 1
#     else:
#         # If the image has 3 channels (RGB), consider it in color
#         color += 1

# print(f"Color images: {color}")
# print(f"Black and white images: {sw}")

# from pdf2image import convert_from_path
# import cv2
# import numpy as np

# # Replace the path with the correct PDF file path
# pdf_path = 'C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/hi this is pdf sample.pdf'

# images = convert_from_path(pdf_path)

# sw = 0
# color = 0

# for image in images:
#     # Convert the PIL image to a NumPy array
#     img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     print("img: ", img)
#     unique_colors = len(np.unique(img))
#     print("unique colors: ", unique_colors)
#     if unique_colors <= 2:
#         # If there are only 1 or 2 unique colors, consider it black and white
#         sw += 1
#     else:
#         # Otherwise, consider it in color
#         color += 1

# print(f"Color images: {color}")
# print(f"Black and white images: {sw}")


import keras.applications as applications
import os
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import tensorflow as tf
from tensorflow import keras
from keras.applications import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input
from keras.preprocessing import image
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing import image

# Load a pre-trained MobileNetV2 model (you can fine-tune this model if needed)
model = MobileNetV2(weights='imagenet')

# Function to classify an image as color or black and white


# def classify_image(file_path):
#     img = image.load_img(file_path, target_size=(224, 224))
#     img = image.img_to_array(img)
#     img = preprocess_input(img)
#     img = np.expand_dims(img, axis=0)

#     predictions = model.predict(img)
#     decoded_predictions = keras.applications.mobilenet_v2.decode_predictions(
#         predictions)
#     top_prediction = decoded_predictions[0][0]

#     # You can adjust this threshold as needed
#     color_threshold = 0.8

#     if top_prediction[2] < color_threshold:
#         return "Black and White"
#     else:
#         return "Color"


def classify_image(file_path):
    img = Image.open(file_path)
    img = img.resize((224, 224))  # Resize the image to the target size
    img = applications.mobilenet_v2.preprocess_input(np.array(img))

    predictions = model.predict(np.expand_dims(img, axis=0))
    decoded_predictions = applications.mobilenet_v2.decode_predictions(
        predictions)
    top_prediction = decoded_predictions[0][0]

    # You can adjust this threshold as needed
    color_threshold = 0.8

    print("pred: ", top_prediction)
    print("thres colr: ", color_threshold)

    if top_prediction[2] < color_threshold:
        return "Black and White"
    else:
        return "Color"


# Replace with the path to your PDF file
pdf_path = 'C:/Users/ASUS/Downloads/DHAVAL FAMILY PRIVATE TRUST/DHAVAL FAMILY PRIVATE TRUST/Dhaval_PMS POA.pdf'

# Extract images from the PDF and classify each one
images = convert_from_path(pdf_path)
for idx, image in enumerate(images):
    image_path = f'image_{idx}.jpg'
    image.save(image_path, 'JPEG')
    result = classify_image(image_path)
    print(f"Page {idx}: {result}")
    os.remove(image_path)  # Delete the temporary image file
