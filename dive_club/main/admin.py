from django.contrib import admin
from .models import Instructor, HomePageContent
from django import forms


class HomePageContentForm(forms.ModelForm):
    class Meta:
        model = HomePageContent
        fields = '__all__'
        widgets = {
            'big_text': forms.Textarea(attrs={
                'rows': 10,  # Установите желаемое количество строк
                'cols': 80,  # Установите желаемое количество столбцов
                'style': 'width: 100%;'  # Ширина на 100%
            }),
            'small_text': forms.Textarea(attrs={
                'rows': 5,
                'cols': 80,
                'style': 'width: 100%;'  # Ширина на 100%
            }),
            'discount_description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 80,
                'style': 'width: 100%;'  # Ширина на 100%
            }),
        }


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'bio', 'avatar')
        }),
    )


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    form = HomePageContentForm

    fieldsets = (
        ('Видео', {
            'fields': ('welcome_video', 'overlay_video_text')
        }),
        ('Фон и текст', {
            'fields': ('background_photo', 'big_text', 'small_text')
        }),
        ('3D модель', {
            'fields': ('diver_model_link',)
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
        """
        Позволяем добавить новый объект только, если его ещё нет.
        Таким образом, в базе всегда будет максимум один объект для главной страницы.
        """
        if self.model.objects.exists():
            return False
        return True
