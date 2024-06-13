#  Copyright 2023 Amazon.com and its affiliates; all rights reserved.
#  This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import os.path
import traceback

from bedrock_chatbot import Chatbot
import pytest
import base64
from PIL import Image
from io import BytesIO


# def image_to_base64(image_path, max_size=2 * 1024 * 1024, step=10):
#     """
#     Convert an image to a Base64 string, ensuring the encoded size is under 5MB.
#
#     Args:
#     image_path (str): Path to the image file.
#     max_size (int, optional): Maximum size in bytes for the Base64-encoded image. Default is 5MB.
#     step (int, optional): Percentage to reduce the dimensions each iteration if resizing is needed. Default is 10%.
#
#     Returns:
#     str: Base64-encoded string of the image.
#     """
#     with Image.open(image_path) as image:
#         # Resize the image if necessary to ensure the resulting base64 string is less than max_size
#         while True:
#             buffered = BytesIO()
#             image.save(buffered, format="PNG")
#             img_bytes = buffered.getvalue()
#             img_base64 = base64.b64encode(img_bytes)
#             if len(img_base64) < max_size:
#                 return img_base64.decode("utf-8")
#             else:
#                 # Reduce the dimensions of the image
#                 current_width, current_height = image.size
#                 new_width = int(current_width * (100 - step) / 100)
#                 new_height = int(current_height * (100 - step) / 100)
#                 # Ensure the new dimensions are not zero
#                 if new_width == 0 or new_height == 0:
#                     raise ValueError("Resizing failed to meet the size requirement.")
#                 image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def image_to_base64(image):
    """
    Convert an image to a Base64 string, ensuring the encoded size is under 5MB.

    Args:
    image (bytes): Bytes of the image file.

    Returns:
    str: Base64-encoded string of the image.
    """

    # Convert the image to a PIL Image object
    image = Image.open(BytesIO(image))

    # Convert RGBA image to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Convert the image to JPEG format
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    jpeg_image = buffer.getvalue()

    # Resize the image if necessary to ensure the resulting base64 string is less than max_size
    max_size = 5 * 1024 * 1024
    step = 10
    while True:
        img_base64 = base64.b64encode(jpeg_image)
        if len(img_base64) < max_size:
            return img_base64.decode("utf-8")
        else:
            # Reduce the dimensions of the image
            current_width, current_height = image.size
            new_width = int(current_width * (100 - step) / 100)
            new_height = int(current_height * (100 - step) / 100)
            # Ensure the new dimensions are not zero
            if new_width == 0 or new_height == 0:
                raise ValueError("Resizing failed to meet the size requirement.")
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def image_to_bytes(image_path):
    """
    Convert an image file to bytes.

    Args:
    image_path (str): Path to the image file.

    Returns:
    bytes: Bytes of the image file.
    """
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    return image_bytes

# @pytest.mark.parametrize(
#     "question",
#     [
#         "write me something about harry potter",
#     ],
# )


def test_ask_stream_with_image():
    try:
        chatbot = Chatbot('anthropic.claude-3-opus-20240229-v1:0')

        question = {
            "text": "What's in this image?",
            "image_data": image_to_base64(
               image_to_bytes("test.png")
            ),
        }

        result = ""
        for chunk in chatbot.ask_stream(question):
            result += chunk

        print(f"result: {result}")
    except Exception as e:
        print(traceback.format_exc())
        raise pytest.fail("DID RAISE {0}".format(e))

