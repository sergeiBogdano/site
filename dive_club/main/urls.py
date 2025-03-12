from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

from django.urls import path
from .views import home

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # Заглушка для страницы "О нас"
    path('training/', views.training, name='training'),  # Заглушка для страницы "Обучение"
    path('equipment/', views.equipment, name='equipment'),  # Заглушка для страницы "Оборудование"
    path('contacts/', views.contacts, name='contacts'),  # Заглушка для страницы "Контакты"
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Заглушка для страницы "Политика конфиденциальности"
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),  # Заглушка для страницы "Условия использования"
    path('gift-certificate/create/', views.gift_certificate_create, name='gift_certificate_create'), # для страницы "подарочные сертификаты"
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
