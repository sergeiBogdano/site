from django.contrib import admin
from .models import (
    Instructor, HomePageContent, Event, EventImage, EquipmentPageContent,
    Equipment, GalleryImage, TrainingPage, TrainingCourse, TrainingImage,
    TrainingVideo, AboutPage, EquipmentCategory, ContactPage, TermsOfService,
    PrivacyPolicy, Application, Certificate
)
from .forms import (
    HomePageContentForm, EquipmentPageContentForm, GalleryImageForm,
)


class BaseAdmin(admin.ModelAdmin):
    """Базовый класс для админки с общими настройками."""
    search_fields = ('title',)
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1


class EventImageInline(admin.TabularInline):
    """Inline для изображений мероприятий."""
    model = EventImage
    extra = 1


class EventInline(admin.TabularInline):
    """Inline для мероприятий на главной странице."""
    model = Event.homepage_content.through
    extra = 1
    verbose_name = "Мероприятие"
    verbose_name_plural = "Мероприятия"


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "validity")
    search_fields = ("title",)


@admin.register(Event)
class EventAdmin(BaseAdmin):
    """Админский интерфейс для мероприятий."""
    inlines = [EventImageInline]
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """Админский интерфейс для инструкторов."""
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'bio', 'avatar', 'room_photo')}),
    )


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    """Админский интерфейс для контента главной страницы."""
    form = HomePageContentForm
    inlines = [EventInline]
    filter_horizontal = ('certificates',)
    fieldsets = (
        ('Видео', {'fields': ('welcome_video', 'overlay_video_text')}),
        ('Фон и текст', {'fields': ('background_photo', 'big_text',
                                    'small_photo', 'small_text')}),
        ('Инструктор', {'fields': ('instructor',)}),
        ('Сертификаты', {'fields': ('certificates',)}),
        ('Скидки', {
            'fields': ('discount_title', 'discount_description',
                       'original_price', 'discounted_price',
                       'discount_percentage', 'discount_validity')
        }),
        ('Описание мероприятий', {'fields': ('event_text',)}),
    )


@admin.register(EquipmentPageContent)
class EquipmentPageContentAdmin(admin.ModelAdmin):
    """Админский интерфейс для контента страницы ремонта оборудования."""
    form = EquipmentPageContentForm
    filter_horizontal = ('equipment',)
    fieldsets = (
        ('Основной контент', {'fields': ('title', 'description', 'background_photo')}),
        ('Оборудование', {'fields': ('equipment',)}),
    )

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    """Админский интерфейс для категорий ремонта оборудования."""
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Админский интерфейс для ремонта оборудования."""
    list_display = ('name', 'category',)
    search_fields = ('name',)
    list_filter = ('category',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'image', 'category', 'detailed_description')}),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Админский интерфейс для галереи изображений."""
    form = GalleryImageForm
    list_display = ('id', 'uploaded_at')
    ordering = ('-uploaded_at',)


class TrainingCourseInline(admin.TabularInline):
    """Inline для курсов обучения на странице TrainingPage."""
    model = TrainingCourse
    extra = 1
    verbose_name = "Курс"
    verbose_name_plural = "Курсы"
    fields = ('title', 'course_category')


@admin.register(TrainingPage)
class TrainingPageAdmin(admin.ModelAdmin):
    """Админский интерфейс для страницы обучения."""
    list_display = ("title",)
    inlines = [TrainingCourseInline]
    fieldsets = (
        ("Основное", {"fields": ("title", "description", "advantages")}),
    )


class TrainingImageInline(admin.TabularInline):
    """Inline для изображений, связанных с курсом обучения."""
    model = TrainingImage
    extra = 1


class TrainingVideoInline(admin.TabularInline):
    """Inline для видео, связанных с курсом обучения."""
    model = TrainingVideo
    extra = 1


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    """Админский интерфейс для курсов обучения."""
    list_display = ('title', 'course_category')
    inlines = [TrainingImageInline, TrainingVideoInline]
    fieldsets = (
        (None, {'fields': ('training_page', 'title', 'course_category', 'description', 'included')}),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Админский интерфейс для страницы 'О нас'."""
    fieldsets = (
        (None, {'fields': ('title', 'introduction', 'team_description', 'team_image',
                           'instructors', 'team_photo', 'mission_statement',
                           'mission_photo', 'mission_image', 'services',
                           'services_image', 'contact_info', 'social_links')}),
    )
    list_display = ('title',)


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    """Админский интерфейс для страницы контактов."""
    list_display = ('address', 'email',)
    search_fields = ('email',)
    list_filter = ('address',)
    fieldsets = (
        ("Основная информация", {"fields": ("address", "phone_numbers", "email")}),
        ("Дополнительно", {"fields": ("map_link", "social_links")}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Админский интерфейс для заявок."""
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    fieldsets = (
        ("Контактные данные", {"fields": ("name", "email", "message")}),
        ("Системная информация", {"fields": ("created_at",)}),
    )
    readonly_fields = ("created_at",)


@admin.register(TermsOfService)
class TermsOfServiceAdmin(BaseAdmin):
    """Админский интерфейс для правил пользования."""
    list_display = ("title",)
    search_fields = ("title", "content")


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(BaseAdmin):
    """Админский интерфейс для политики конфиденциальности."""
    list_display = ("title",)
    search_fields = ("title", "content")
