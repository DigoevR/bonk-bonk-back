from rest_framework.serializers import ValidationError
from django.core.files.images import get_image_dimensions

from constants import MEGABYTE_LIMIT

def max_image_size_validator(image):
    filesize = image.size
    width, height = get_image_dimensions(image)

    if filesize > MEGABYTE_LIMIT * 1024 * 1024:
        raise ValidationError(f"Max file size is {MEGABYTE_LIMIT}MB")
