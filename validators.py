import base64
import binascii

from exceptions import ValidationError


def validate_base64_image(base64_string: str) -> bytes:
    try:
        decoded_image = base64.b64decode(base64_string)
    except (binascii.Error, binascii.Incomplete, UnicodeDecodeError):
        raise ValidationError
    return decoded_image
