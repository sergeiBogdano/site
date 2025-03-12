from django import forms
from .models import MainBanner, PageBlock, News, Testimonial, SiteSettings

class MainBannerForm(forms.ModelForm):
    class Meta:
        model = MainBanner
        fields = '__all__'


class PageBlockForm(forms.ModelForm):
    class Meta:
        model = PageBlock
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'