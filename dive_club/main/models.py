import os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
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


# Инструктор
class Instructor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя инструктора")
    bio = models.TextField(verbose_name="Биография инструктора")
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар инструктора"
    )
    room_photo = models.ImageField(
        upload_to='instructors/',
        blank=True,
        null=True,
        verbose_name="Помещение"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Инструктор"
        verbose_name_plural = "Инструкторы"


# Контент главной страницы
class HomePageContent(models.Model):
    # Поля для видео
    welcome_video = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True,
        verbose_name="Видео приветствия",
        validators=[validate_video_file_size, validate_file_extension]
    )
    # Поля для основного контента
    background_photo = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name="Большое изображение",
        validators=[validate_image_file_size, validate_file_extension]
    )
    big_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Большой текст (на первой фотографии)"
    )
    small_photo = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name="Малое изображение",
        validators=[validate_image_file_size, validate_file_extension]
    )
    small_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Малый текст"
    )
    overlay_video_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Текст на видео"
    )
    # Поля для инструктора
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Инструктор"
    )
    # Поля для подарочных сертификатов
    certificate_image = models.ImageField(
        upload_to='certificates/',
        blank=True,
        null=True,
        verbose_name="Изображение сертификата",
        validators=[validate_image_file_size, validate_file_extension]
    )
    certificate_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Название сертификата"
    )
    certificate_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание сертификата"
    )
    certificate_validity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Срок действия сертификата"
    )
    certificate_terms = models.TextField(
        blank=True,
        null=True,
        verbose_name="Условия использования сертификата"
    )
    certificate_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена сертификата"
    )
    event_text = models.CharField(
        max_length=100,
        verbose_name="Описание мероприятий",
        blank=True,
        null=True
    )
    # Поля для скидок
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
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Процент скидки",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    discount_validity = models.DateField(
        blank=True,
        null=True,
        verbose_name="Срок действия скидки"
    )

    def __str__(self):
        return "Контент главной страницы"

    class Meta:
        verbose_name = "Контент главной страницы"
        verbose_name_plural = "Контент главной страницы"


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание мероприятия", blank=True, null=True)
    homepage_content = models.ManyToManyField(
        HomePageContent,
        related_name='events',
        verbose_name="Контент главной страницы",
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


# Изображения для мероприятия
class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='events/',
        validators=[validate_image_file_size, validate_file_extension]
    )

    def __str__(self):
        return f"{self.event.title} - Image"


# Оборудование
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
    equipment = models.ManyToManyField(
        Equipment,
        related_name="equipment_page",
        blank=True,
        verbose_name="Список оборудования"
    )

    def __str__(self):
        return "Контент страницы оборудования"

    class Meta:
        verbose_name = "Контент страницы оборудования"
        verbose_name_plural = "Контент страницы оборудования"


# Фотогалерея
class GalleryImage(models.Model):
    image = models.ImageField(
        upload_to="gallery/",
        validators=[validate_image_file_size, validate_file_extension]
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Галерея"
        verbose_name_plural = "Галерея"

    def __str__(self):
        return f"Фото {self.id} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"


# Страница обучения
class TrainingPage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание страницы")
    advantages = models.TextField(verbose_name="Преимущества обучения")
    course_prices = models.TextField(verbose_name="Цены на курсы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница обучения"
        verbose_name_plural = "Страница обучения"


# Отдельная модель курсов, разделённых по уровням
class TrainingCourse(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Курсы для новичков'),
        ('advanced', 'Продвинутые курсы'),
        ('professional', 'Профессиональные курсы'),
        ('tech', 'Технический дайвинг'),
    ]
    training_page = models.ForeignKey(TrainingPage, on_delete=models.CASCADE, related_name="courses")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень курса")
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")

    def __str__(self):
        return f"{self.get_level_display()}: {self.title}"


# Изображения для страницы обучения
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


# Видео для страницы обучения
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


# Страница "О нас"
class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    introduction = models.TextField(verbose_name="Введение")
    # Команда
    team_description = models.TextField(verbose_name="Описание команды", blank=True, null=True)
    team_image = models.ImageField(
        upload_to='about/team/',
        verbose_name="Изображение команды",
        blank=True,
        null=True
    )
    instructors = models.ManyToManyField(Instructor, blank=True, verbose_name="Инструкторы")
    team_photo = models.ImageField(
        upload_to='about/team/',
        blank=True,
        null=True,
        verbose_name="Фото команды",
        validators=[validate_image_file_size, validate_file_extension]
    )
    # Миссия и услуги
    mission_statement = models.TextField(verbose_name="Наша миссия")
    mission_photo = models.ImageField(
        upload_to='about/mission/',
        blank=True,
        null=True,
        verbose_name="Фото миссии",
        validators=[validate_image_file_size, validate_file_extension]
    )
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
    # Контакты
    contact_info = models.TextField(verbose_name="Связь с нами")
    social_links = models.JSONField(verbose_name="Ссылки на соцсети", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


# Страница контактов
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


# Правила пользования
class TermsOfService(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Правила пользования"
        verbose_name_plural = "Правила пользования"

    def __str__(self):
        return "Правила пользования"


# Политика конфиденциальности
class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

    def __str__(self):
        return "Политика конфиденциальности"


# Заявки
class Application(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заявка от {self.name}'

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
