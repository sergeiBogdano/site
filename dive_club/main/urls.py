from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # Страница "О нас"
    path('training/', views.training, name='training'),  # Страница "Обучение"
    path('equipment/', views.equipment, name='equipment'),  # Страница "Оборудование"
    path('contacts/', views.contacts, name='contacts'),  # Страница "Контакты"
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Политика конфиденциальности
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),  # Условия использования
    path('gift-certificate/create/', views.gift_certificate_create, name='gift_certificate_create'),  # Подарочные сертификаты
    path('gallery/', views.gallery, name='gallery'),
    path('apply/', views.application_view, name='application'),
    path('apply/success/', views.application_success, name='application_success'),
    path('event/create/', views.event_create, name='event_create'),# Добавлен путь для создания мероприятия
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
                  # Новый маршрут для деталей мероприятия
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)