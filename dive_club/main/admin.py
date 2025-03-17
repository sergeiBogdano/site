from django.contrib import admin
from .models import (
    Instructor, HomePageContent,
    Event, EventImage,
    EquipmentPageContent,
    Equipment, GalleryImage,
    TrainingPage, TrainingImage,
    TrainingVideo, AboutPage,
    ContactPage, TermsOfService,
    PrivacyPolicy, Application
)
from .forms import (
    HomePageContentForm,
    EquipmentPageContentForm,
    EquipmentForm,
    GalleryImageForm,
    ContactPageForm

)


def has_add_permission(self, request):
    if self.model.objects.exists():
        return False
    return True


def has_change_permission(self, request, obj=None):
    return True

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1  # Количество пустых форм для добавления


class EventInline(admin.TabularInline):  # Используем TabularInline для отображения событий
    model = Event
    extra = 1  # Количество дополнительных пустых форм для добавления новых событий

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline]

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'bio', 'avatar', 'room_photo')
        }),
    )


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    form = HomePageContentForm
    inlines = [EventInline]  # Добавляем возможность редактировать события в HomePageContent

    fieldsets = (
        ('Видео', {
            'fields': ('welcome_video', 'overlay_video_text')
        }),
        ('Фон и текст', {
            'fields': ('background_photo', 'big_text', 'small_text')
        }),
        ('Инструктор', {
            'fields': ('instructor',)
        }),
        ('Скидки', {
            'fields': ('discount_title', 'discount_description', 'discount_percentage', 'original_price', 'discounted_price'),
        }),
        ('Подарочные сертификаты', {
            'fields': ('certificate_image', 'tg_id')
        }),
    )

@admin.register(EquipmentPageContent)
class EquipmentPageContentAdmin(admin.ModelAdmin):
    form = EquipmentPageContentForm
    filter_horizontal = ('equipment',)  # для удобства выбора оборудования
    fieldsets = (
        ('Основной контент', {
            'fields': ('title', 'description', 'background_photo')
        }),
        ('Оборудование', {
            'fields': ('equipment',)
        }),
    )

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    form = EquipmentForm
    list_display = ('name',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image')
        }),
    )

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageForm
    list_display = ('id', 'uploaded_at')
    ordering = ('-uploaded_at',)

class TrainingImageInline(admin.TabularInline):
    model = TrainingImage
    extra = 1  # Позволяет загружать несколько изображений

class TrainingVideoInline(admin.TabularInline):
    model = TrainingVideo
    extra = 1  # Позволяет загружать несколько видео


@admin.register(TrainingPage)
class TrainingPageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TrainingImageInline, TrainingVideoInline]  # Добавляем изображения и видео

    fieldsets = (
        ("Основное", {"fields": ("title", "description")}),
        ("Курсы", {"fields": ("beginner_courses", "advanced_courses", "professional_courses", "tech_courses")}),
        ("Преимущества", {"fields": ("advantages",)}),
        ("Стоимость", {"fields": ("course_prices",)}),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'introduction',
                'team_description',
                'team_image',
                'instructors', # Поле для изображения команды
                'services',
                'services_image',  # Поле для изображения услуг
                'contact_info',
                'facebook_link',
                'instagram_link',
            )
        }),
    )

    list_display = ('title',)


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('address', 'email',)
    fieldsets = (
        ("Основная информация", {
            "fields": ("address", "phone_numbers", "email")
        }),
        ("Дополнительно", {
            "fields": ("map_link", "social_links")
        }),
    )

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактные данные"



admin.site.register(TermsOfService)
admin.site.register(PrivacyPolicy)
admin.site.register(Application)