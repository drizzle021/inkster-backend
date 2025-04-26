import uuid
import base64
import os
from io import BytesIO
from datetime import datetime
from PIL import Image as PILImage

# 2 MBs
MAX_FILESIZE = 1024*1024*2

def encode_filename(filename):
    """
    Encodes filename into unique filenames with 42-43 chars
    """
    unique_id = uuid.uuid4()
    base64_id = base64.urlsafe_b64encode(unique_id.bytes).decode("utf-8").rstrip("=")
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    
    _, extension = os.path.splitext(filename)
    extension = extension.lstrip(".") or "jpg"

    return f"{base64_id}_{timestamp}.{extension}"


def validate_filename(filename):
    """
    Check if the given file has a valid extension.
    Ensures the files matches the allowed formats.
    """

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
    if "." not in filename:
        return False
    

    _, extension = os.path.splitext(filename)
    extension = extension.lstrip(".")

    if extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
    
def normalize_image(image_file, target_width=800, target_height=600):
    """
    Normalizes the image resolution (WxH) while retaining aspect ratio.
    """
    with PILImage.open(image_file) as img:
        img.thumbnail((target_width, target_height))
        normalized_image = BytesIO()
        img.save(normalized_image, format=img.format)
        normalized_image.seek(0)
        return normalized_image

def validate_file_size(image_file):
    """
    Validates file size based on the set limit by MAX_FILESIZE
    """
    image_file.seek(0, os.SEEK_END)
    file_size = image_file.tell()
    image_file.seek(0)
    return file_size <= MAX_FILESIZE