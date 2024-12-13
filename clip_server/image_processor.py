from PIL import Image
import pillow_heif
import base64
from io import BytesIO

# Register HEIC support
pillow_heif.register_heif_opener()

def encode_image(filename):
    """
    Encode image into a base64 string
    """
    # Load image data
    with open(filename, 'rb') as image_file:
        image_data = image_file.read()

    # Encode image to Base64 string
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    return image_base64

def decode_image(image_base64):
    """
    Decode base64 string into PIL.Image object
    """
    # Decode Base64 string to binary image data
    image_data = base64.b64decode(image_base64)

    # Create a BytesIO object to work with in-memory binary data
    image_bytes = BytesIO(image_data)

    # Open the image using PIL.Image (with HEIC support)
    image_pil = Image.open(image_bytes)

    return image_pil
