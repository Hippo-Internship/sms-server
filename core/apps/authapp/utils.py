# Python imports
from uuid import uuid4
import os
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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