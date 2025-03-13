import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

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


# Модель для оборудования (все в одной записи)
class Equipment(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название оборудования")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to='equipment/',
        validators=[validate_image_file_size, validate_file_extension],
        verbose_name="Изображение"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


# Контент страницы оборудования
class EquipmentPageContent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок страницы", default="Снаряжение для дайвинга")
    description = models.TextField(verbose_name="Описание страницы", blank=True, null=True)
    background_photo = models.ImageField(
        upload_to='equipment_page/',
        blank=True,
        null=True,
        verbose_name="Фоновое изображение",
        validators=[validate_image_file_size, validate_file_extension]
    )
    equipment = models.ManyToManyField(Equipment, related_name="equipment_page", blank=True, verbose_name="Список оборудования")

    def __str__(self):
        return "Контент страницы оборудования"

    class Meta:
        verbose_name = "Контент страницы оборудования"
        verbose_name_plural = "Контент страницы оборудования"


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Фото {self.id} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галерея"


class TrainingPage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание страницы")

    # Уровни курсов
    beginner_courses = models.TextField(verbose_name="Курсы для новичков")
    advanced_courses = models.TextField(verbose_name="Продвинутые курсы")
    professional_courses = models.TextField(verbose_name="Профессиональные курсы")
    tech_courses = models.TextField(verbose_name="Технический дайвинг")

    advantages = models.TextField(verbose_name="Преимущества обучения")

    # Стоимость
    course_prices = models.TextField(verbose_name="Цены на курсы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница обучения"
        verbose_name_plural = "Страница обучения"


class TrainingImage(models.Model):
    training_page = models.ForeignKey(
        TrainingPage, on_delete=models.CASCADE, related_name="images", verbose_name="Страница обучения"
    )
    image = models.ImageField(
        upload_to="training_images/",
        validators=[validate_image_file_size, validate_file_extension],
        verbose_name="Изображение"
    )

    def __str__(self):
        return f"Изображение для {self.training_page.title}"

    class Meta:
        verbose_name = "Изображение обучения"
        verbose_name_plural = "Изображения обучения"


class TrainingVideo(models.Model):
    training_page = models.ForeignKey(
        TrainingPage, on_delete=models.CASCADE, related_name="videos", verbose_name="Страница обучения"
    )
    video = models.FileField(
        upload_to="training_videos/",
        validators=[validate_video_file_size, validate_file_extension],
        verbose_name="Видео"
    )

    def __str__(self):
        return f"Видео для {self.training_page.title}"

    class Meta:
        verbose_name = "Видео обучения"
        verbose_name_plural = "Видео обучения"


class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    introduction = models.TextField(verbose_name="Введение")

    # Поля для команды
    team_description = models.TextField(verbose_name="Описание команды", blank=True, null=True)
    team_image = models.ImageField(upload_to='about/team/', verbose_name="Изображение команды", blank=True, null=True)
    instructors = models.ManyToManyField(Instructor, blank=True, verbose_name="Инструкторы")
    # Поля для услуг
    services = models.TextField(verbose_name="Наши услуги", blank=True, null=True)
    services_image = models.ImageField(upload_to='about/services/', verbose_name="Изображение услуг", blank=True,
                                       null=True)

    contact_info = models.TextField(verbose_name="Связь с нами", blank=True, null=True)
    facebook_link = models.URLField(verbose_name="Ссылка на Facebook", blank=True, null=True)
    instagram_link = models.URLField(verbose_name="Ссылка на Instagram", blank=True, null=True)

    team_photo = models.ImageField(
        upload_to='about/team/',
        blank=True,
        null=True,
        verbose_name="Фото команды",
        validators=[validate_image_file_size, validate_file_extension]
    )

    mission_photo = models.ImageField(
        upload_to='about/mission/',
        blank=True,
        null=True,
        verbose_name="Фото миссии",
        validators=[validate_image_file_size, validate_file_extension]
    )

    mission_statement = models.TextField(verbose_name="Наша миссия")
    mission_image = models.ImageField(
        upload_to='about/mission_image/',
        blank=True,
        null=True,
        verbose_name="Изображение миссии",
        validators=[validate_image_file_size, validate_file_extension]
    )

    services = models.TextField(verbose_name="Наши услуги")
    services_image = models.ImageField(
        upload_to='about/services_image/',
        blank=True,
        null=True,
        verbose_name="Изображение услуг",
        validators=[validate_image_file_size, validate_file_extension]
    )

    contact_info = models.TextField(verbose_name="Связь с нами")
    social_links = models.JSONField(verbose_name="Ссылки на соцсети", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class ContactPage(models.Model):
    address = models.CharField("Адрес", max_length=255)
    phone_numbers = models.JSONField("Телефонные номера", default=list)  # Список номеров
    email = models.EmailField("Электронная почта")
    map_link = models.URLField("Ссылка на карту")  # Ссылка на карту
    social_links = models.JSONField("Социальные сети", default=dict)  # Ссылки на соцсети

    class Meta:
        verbose_name = "Контактная страница"
        verbose_name_plural = "Контактные страницы"

    def __str__(self):
        return "Контактная информация"