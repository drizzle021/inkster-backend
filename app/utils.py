import uuid
import base64
import os
from datetime import datetime

def endcode_filename(filename):
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