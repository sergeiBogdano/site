from django.contrib import admin
from .models import Instructor, HomePageContent, Event, EventImage
from django import forms


class HomePageContentForm(forms.ModelForm):
    class Meta:
        model = HomePageContent
        fields = '__all__'
        widgets = {
            'big_text': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80,
                'style': 'width: 100%;'
            }),
            'small_text': forms.Textarea(attrs={
                'rows': 5,
                'cols': 80,
                'style': 'width: 100%;'
            }),
            'discount_description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 80,
                'style': 'width: 100%;'
            }),
            'event_text': forms.Textarea(attrs={
                'rows': 5,
                'cols': 80,
                'style': 'width: 100%;'
            }),
        }

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

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        return True
