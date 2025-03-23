from django.contrib import admin
from .models import (
    Instructor, HomePageContent,
    Event, EventImage,
    EquipmentPageContent,
    Equipment, GalleryImage,
    TrainingPage, TrainingCourse, TrainingImage, TrainingVideo,
    AboutPage,
    ContactPage, TermsOfService,
    PrivacyPolicy, Application
)
from .forms import (
    HomePageContentForm,
    EquipmentPageContentForm,
    EquipmentForm,
    GalleryImageForm,
)


class ReadOnlyAdmin(admin.ModelAdmin):
    """Базовый класс для объектов, где можно редактировать, но не добавлять новые."""
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_change_permission(self, request, obj=None):
        return True


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


class EventInline(admin.TabularInline):
    model = Event.homepage_content.through
    extra = 1
    verbose_name = "Мероприятие"
    verbose_name_plural = "Мероприятия"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'bio', 'avatar', 'room_photo')}),
    )


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):  # Используем ModelAdmin вместо ReadOnlyAdmin
    form = HomePageContentForm
    inlines = [EventInline]
    fieldsets = (
        ('Видео', {
            'fields': ('welcome_video', 'overlay_video_text')
        }),
        ('Фон и текст', {
            'fields': ('background_photo', 'big_text', 'small_photo', 'small_text')
        }),
        ('Инструктор', {
            'fields': ('instructor',)
        }),
        ('Подарочные сертификаты', {
            'fields': (
                'certificate_image', 'certificate_title', 'certificate_description',
                'certificate_validity', 'certificate_terms', 'certificate_price'
            )
        }),
        ('Скидки', {
            'fields': (
                'discount_title', 'discount_description', 'original_price',
                'discounted_price', 'discount_percentage', 'discount_validity'
            )
        }),
        ('Описание мероприятий', {
            'fields': ('event_text',)
        }),
    )


@admin.register(EquipmentPageContent)
class EquipmentPageContentAdmin(ReadOnlyAdmin):
    form = EquipmentPageContentForm
    filter_horizontal = ('equipment',)
    fieldsets = (
        ('Основной контент', {'fields': ('title', 'description', 'background_photo')}),
        ('Оборудование', {'fields': ('equipment',)}),
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    form = EquipmentForm
    list_display = ('name',)
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'image')}),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageForm
    list_display = ('id', 'uploaded_at')
    ordering = ('-uploaded_at',)


class TrainingCourseInline(admin.TabularInline):
    model = TrainingCourse
    extra = 1
    verbose_name = "Курс"
    verbose_name_plural = "Курсы"


class TrainingImageInline(admin.TabularInline):
    model = TrainingImage
    extra = 1


class TrainingVideoInline(admin.TabularInline):
    model = TrainingVideo
    extra = 1


@admin.register(TrainingPage)
class TrainingPageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TrainingCourseInline, TrainingImageInline, TrainingVideoInline]
    fieldsets = (
        ("Основное", {"fields": ("title", "description", "advantages", "course_prices")}),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title', 'introduction', 'team_description', 'team_image',
                'instructors', 'team_photo',
                'mission_statement', 'mission_photo', 'mission_image',
                'services', 'services_image', 'contact_info', 'social_links'
            )
        }),
    )
    list_display = ('title',)


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('address', 'email',)
    fieldsets = (
        ("Основная информация", {"fields": ("address", "phone_numbers", "email")}),
        ("Дополнительно", {"fields": ("map_link", "social_links")}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    fieldsets = (
        ("Контактные данные", {"fields": ("name", "email", "message")}),
        ("Системная информация", {"fields": ("created_at",)}),
    )
    readonly_fields = ("created_at",)


admin.site.register(TermsOfService)
admin.site.register(PrivacyPolicy)
