"""Contains project-wide utilities"""

# import os
# from django.conf import settings
from django.contrib.contenttypes.models import ContentType
# from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
# from django.utils.translation import gettext_lazy as _

from core.constants import FILE_STORAGE_CLASS

STORAGE = FILE_STORAGE_CLASS()


def get_content_type(model_or_obj):
    """Return the content type of a given model"""
    
    return ContentType.objects.get_for_model(model_or_obj)


# def get_file_path(file):
#     """
#     Get file path of file object or uploaded file. If `uploaded_file` is in 
#     memory(InMemoryUploadedFile), save it to a temporary folder and return that path.
#     """
#     if isinstance(file, TemporaryUploadedFile):
#         print("temporary uploaded file")
#         path = file.temporary_file_path()
#     elif isinstance(file, InMemoryUploadedFile):
#         print('in memory uploaded file')
#         # Store file in temporary directory first
#         path = os.path.join(settings.MEDIA_ROOT, TEMP_FILES_UPLOAD_DIR, file.name)

#         # If file doesn't exist, save it 
#         if not STORAGE.exists(path):
#             print('file does not exist, saving it')

#             with STORAGE.open(path, 'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#     else:
#         path = file.path

#     print(path)
#     return path


# def get_file_extension(file) -> str:
#     """Return file extension"""
#     return file.name.split('.')[-1].lower()
    


