# Python imports
from uuid import uuid4
import os
from PIL import Image
import sys
from io import BytesIO
# Django built-in imports
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible
from django.conf import settings



@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path, field="image"):
        self.path = sub_path
        self.field = field

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        old_image = getattr(instance, self.field, instance.image)
        old_image_file_path = os.path.join(settings.MEDIA_ROOT, self.path, old_image.name)
        if os.path.exists(old_image_file_path):
            os.remove(old_image_file_path)
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)

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