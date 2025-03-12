import os
from django.db import models
from django.core.exceptions import ValidationError

# Валидация для изображений
def validate_image_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('Максимальный размер файла 5MB')

# Валидация для видео
def validate_video_file_size(value):
    limit = 50 * 1024 * 1024  # 50 MB
    if value.size > limit:
        raise ValidationError('Максимальный размер файла 50MB')

# Валидация для форматов файлов
def validate_file_extension(value):
    valid_extensions = ['.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png']
    extension = os.path.splitext(value.name)[1].lower()
    if extension not in valid_extensions:
        raise ValidationError('Недопустимый формат файла. Разрешены: ' + ', '.join(valid_extensions))


class Instructor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя инструктора")
    bio = models.TextField(verbose_name="Биография инструктора")
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар инструктора"
    )
    room_photo = models.ImageField(upload_to='instructors/', blank=True, null=True, verbose_name="Помещение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Инструктор"
        verbose_name_plural = "Инструкторы"


class HomePageContent(models.Model):
    welcome_video = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True,
        verbose_name="Видео приветствия",
        validators=[validate_video_file_size, validate_file_extension]
    )

    background_photo = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name="Фоновое изображение",
        validators=[validate_image_file_size, validate_file_extension]
    )

    big_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Большой текст (на первой фотографии)"
    )

    small_text = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Малый текст"
    )

    overlay_video_text = models.CharField(  # Новое поле для текста на видео
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Текст на видео"
    )

    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Инструктор"
    )

    # Новые поля для скидок
    discount_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Название скидки"
    )

    discount_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание скидки"
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Процент скидки"
    )

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена без скидки"
    )

    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена со скидкой"
    )

    # Новые поля для подарочных сертификатов
    certificate_image = models.ImageField(
        upload_to='certificates/',
        blank=True,
        null=True,
        verbose_name="Изображение сертификата",
        validators=[validate_image_file_size, validate_file_extension]
    )

    tg_id = models.CharField(
        max_length=100,
        verbose_name="Telegram ID",
        blank=True,
        null=True
    )

    event_text = models.CharField(
        max_length=100,
        verbose_name="Описание мероприятий",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Контент главной страницы"

    class Meta:
        verbose_name = "Контент главной страницы"
        verbose_name_plural = "Контент главной страницы"


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание мероприятия", blank=True, null=True)

    # Сделаем внешний ключ nullable
    homepage_content = models.ForeignKey(
        HomePageContent,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name="Контент главной страницы",
        null=True  # Разрешаем null для существующих записей
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/', validators=[validate_image_file_size, validate_file_extension])

    def __str__(self):
        return f"{self.event.title} - Image"
