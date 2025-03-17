from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # для страницы "О нас"
    path('training/', views.training, name='training'),  # для страницы "Обучение"
    path('equipment/', views.equipment, name='equipment'),  # для страницы "Оборудование"
    path('contacts/', views.contacts, name='contacts'),  # для страницы "Контакты"
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # для страницы "Политика конфиденциальности"
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),  # для страницы "Условия использования"
    path('gift-certificate/create/', views.gift_certificate_create, name='gift_certificate_create'), # для страницы "подарочные сертификаты"
    path('gallery/', views.gallery, name='gallery'),
    path('apply/', views.application_view, name='application'),
    path('apply/success/', views.application_success, name='application_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
