# Python imports
from uuid import uuid4
import os
from PIL import Image
import sys
from io import BytesIO
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import InMemoryUploadedFile

User = get_user_model()

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        print(instance)
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)
    return wrapper

def compress_image(image):
    im = Image.open(image)
    output = BytesIO()
    im.save(output, format=im.format, quality=20)
    output.seek(0)
    return InMemoryUploadedFile(
        output, 
        'ImageField', "%s.png" % image.name.split('.')[0], 'image/png',
        sys.getsizeof(output), 
        None
    )

def can_user_manage(user_groups: Group, request_groups: Group, user: User=None, request_user: User=None):
    user_allowed_access = User.ALLOWED_USER_MANAGEMENT[user_groups.role_id]
    operation = user_allowed_access[0] if len(user_allowed_access) > 0 else None
    if (operation == "*" or
        operation == "-" and request_groups.role_id not in user_allowed_access or
        operation == "+" and request_groups.role_id in user_allowed_access):
        return True
    return user is not None and request_user is not None and user.id == request_user.id