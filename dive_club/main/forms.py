from django import forms
from .models import HomePageContent, Equipment, EquipmentPageContent, GalleryImage


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


class EquipmentForm(forms.ModelForm):
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

# Форма для модели EquipmentPageContent
class EquipmentPageContentForm(forms.ModelForm):
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
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = GalleryImage
        fields = ['images']  # Оставляем только поле для загрузки

    def save(self, commit=True):
        images = self.files.getlist('images')
        for image in images:
            GalleryImage.objects.create(image=image)
        return super().save(commit=False)