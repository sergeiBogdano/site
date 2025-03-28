import os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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


class Instructor(models.Model):
    """Модель инструктора."""
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


class HomePageContent(models.Model):
    """Контент главной страницы."""
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
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Инструктор"
    )
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
    """Модель мероприятия."""
    title = models.CharField(max_length=100, verbose_name="Название мероприятия")
    description = models.TextField(
        verbose_name="Описание мероприятия",
        blank=True,
        null=True
    )
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


class EventImage(models.Model):
    """Изображения для мероприятия."""
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='events/',
        validators=[validate_image_file_size, validate_file_extension]
    )

    def __str__(self):
        return f"{self.event.title} - Image"


class EquipmentCategory(models.Model):
    """Категория оборудования."""
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = "Категории оборудования"


class Equipment(models.Model):
    """Модель оборудования."""
    name = models.CharField(max_length=100, verbose_name="Название оборудования")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to='equipment/',
        validators=[validate_image_file_size, validate_file_extension],
        verbose_name="Изображение"
    )
    category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class EquipmentPageContent(models.Model):
    """Контент страницы оборудования."""
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок страницы",
        default="Снаряжение для дайвинга"
    )
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


class GalleryImage(models.Model):
    """Фотогалерея."""
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


class TrainingPage(models.Model):
    """Страница обучения"""
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание страницы")
    advantages = models.TextField(verbose_name="Преимущества обучения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница обучения"
        verbose_name_plural = "Страницы обучения"


class TrainingCourse(models.Model):
    """Курс обучения с категориями."""
    CATEGORY_CHOICES = [
        ('regular', 'Обычные курсы'),
        ('sdi_specialization', 'Специализации SDI'),
        ('first_response', 'Курсы первой медицинской помощи'),
    ]
    training_page = models.ForeignKey(
        TrainingPage,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Страница обучения"
    )
    title = models.CharField(max_length=255, verbose_name="Название курса")
    course_category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='regular',
        verbose_name="Тип курса"
    )
    description = models.TextField(verbose_name="Описание курса")
    included = models.TextField(verbose_name="Что входит в курс")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс обучения"
        verbose_name_plural = "Курсы обучения"


class TrainingImage(models.Model):
    """Изображения, связанные с курсами обучения."""
    course = models.ForeignKey(
        TrainingCourse,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        verbose_name="Курс"
    )
    image = models.ImageField(
        upload_to="training_images/",
        verbose_name="Изображение курса"
    )

    def __str__(self):
        return f"Изображение для {self.course.title}"

    class Meta:
        verbose_name = "Изображение курса"
        verbose_name_plural = "Изображения курсов"


class TrainingVideo(models.Model):
    """Видео для курсов обучения."""
    course = models.ForeignKey(
        TrainingCourse,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Курс"
    )
    video = models.FileField(
        upload_to="training_videos/",
        verbose_name="Видео курса"
    )

    def __str__(self):
        return f"Видео для {self.course.title}"

    class Meta:
        verbose_name = "Видео курса"
        verbose_name_plural = "Видео курсов"


class AboutPage(models.Model):
    """Страница 'О нас'."""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    introduction = models.TextField(verbose_name="Введение")
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
    contact_info = models.TextField(verbose_name="Связь с нами")
    social_links = models.JSONField(verbose_name="Ссылки на соцсети", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class ContactPage(models.Model):
    """Страница контактов."""
    address = models.CharField("Адрес", max_length=255)
    phone_numbers = models.JSONField("Телефонные номера", default=list)
    email = models.EmailField("Электронная почта")
    map_link = models.URLField("Ссылка на карту")
    social_links = models.JSONField("Социальные сети", default=dict)

    class Meta:
        verbose_name = "Контактная страница"
        verbose_name_plural = "Контактные страницы"

    def __str__(self):
        return "Контактная информация"


class TermsOfService(models.Model):
    """Правила пользования."""
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Правила пользования"
        verbose_name_plural = "Правила пользования"

    def __str__(self):
        return "Правила пользования"


class PrivacyPolicy(models.Model):
    """Политика конфиденциальности."""
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

    def __str__(self):
        return "Политика конфиденциальности"


class Application(models.Model):
    """Модель заявки."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заявка от {self.name}'

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
