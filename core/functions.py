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
from django.core.files.storage import default_storage

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path, field="image"):
        self.path = sub_path
        self.field = field

    def __call__(self, instance, filename):
        print("dwqwdq")
        ext = filename.split('.')[-1]
        old_image = getattr(instance, self.field, instance.image)
        print(filename, old_image, instance.pk)
        if filename == old_image:
            return os.path.join(self.path, filename)
        # old_image_file_path = os.path.join(settings.MEDIA_ROOT, self.path, old_image.name)
        # print(old_image)
        # print(old_image_file_path)

        # if os.path.exists(old_image_file_path):
        #     os.remove(old_image_file_path)
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

def handle_image_upload(instance, real_instance, field, path=""):
    new_file = getattr(instance, field)
    filename = new_file.name.split(".") if new_file.name is not None else None
    if not instance.pk:
        return False
    old_file = getattr(real_instance, field)
    if not old_file.name.split("/")[-1] == new_file.name:
        if old_file and default_storage.exists(old_file.name):
            default_storage.delete(old_file.name)
        if new_file.name is not None:
            new_file.name = '{}.{}'.format(uuid4().hex, filename[-1])
    else:
        setattr(instance, field, old_file)
    return True