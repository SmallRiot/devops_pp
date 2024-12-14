import os
from PIL import Image

from rest_framework import serializers
from core.models import Document
import logging


logger = logging.getLogger(__name__)

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['path']

    def validate_path(self, value):
        file_extension = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.jpeg', '.jpg', '.heic', '.heif', '.png', '.pdf']

        if file_extension not in allowed_extensions:
            logger.warning("Attempt to upload a file with an unsupported extension: %s", value.name)
            raise serializers.ValidationError("Разрешены только файлы в форматах JPEG, JPG, PDF, HEIF/HEIC и PNG")

        return value