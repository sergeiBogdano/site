from django import forms
from .models import (
    HomePageContent, Equipment, EquipmentPageContent,
    GalleryImage, ContactPage, Application
)


class HomePageContentForm(forms.ModelForm):
    """Форма для редактирования контента главной страницы."""

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


class EquipmentForm(forms.ModelForm):
    """Форма для редактирования оборудования."""

    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 80,
                'style': 'width: 100%;'
            }),
        }


class EquipmentPageContentForm(forms.ModelForm):
    """Форма для редактирования контента страницы оборудования."""

    class Meta:
        model = EquipmentPageContent
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width: 100%;'
            }),
            'description': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80,
                'style': 'width: 100%;'
            }),
        }


class GalleryImageForm(forms.ModelForm):
    """Форма для загрузки изображений в галерею."""

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = GalleryImage
        fields = ['images']

    def save(self, commit=True):
        images = self.files.getlist('images')
        for image in images:
            GalleryImage.objects.create(image=image)
        return super().save(commit=False)


class ContactPageForm(forms.ModelForm):
    """Форма для редактирования контактной информации."""

    class Meta:
        model = ContactPage
        fields = ['address', 'phone_numbers', 'email', 'social_links']


class ApplicationForm(forms.ModelForm):
    """Форма для подачи заявки."""

    class Meta:
        model = Application
        fields = ['name', 'email', 'message']
