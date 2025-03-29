import os
from django.core.exceptions import ValidationError


def validate_image_file_size(value):
    """Валидация размера изображения (максимум 5 MB)."""
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('Максимальный размер файла 5MB')


def validate_video_file_size(value):
    """Валидация размера видео (максимум 50 MB)."""
    limit = 50 * 1024 * 1024  # 50 MB
    if value.size > limit:
        raise ValidationError('Максимальный размер файла 50MB')


def validate_file_extension(value):
    """Валидация форматов файлов."""
    valid_extensions = ['.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png']
    extension = os.path.splitext(value.name)[1].lower()
    if extension not in valid_extensions:
        raise ValidationError(
            'Недопустимый формат файла. Разрешены: ' + ', '.join(valid_extensions)
        )