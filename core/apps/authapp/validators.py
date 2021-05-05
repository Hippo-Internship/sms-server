# Python imports
import re
# Django buil-in imports
from django.core.exceptions import ValidationError

def validate_phone(value):
    if re.match("^[8-9]\d{7}$", value) is None:
        raise ValidationError("Phone number is not valid!")
    return