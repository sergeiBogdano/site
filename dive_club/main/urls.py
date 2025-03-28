from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # Страница "О нас"
    path('training/', views.training, name='training'),  # Страница "Обучение"
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path('equipment/', views.equipment_list, name='equipment_list'),  # Страница "Оборудование"
    path('contacts/', views.contacts, name='contacts'),  # Страница "Контакты"
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Политика конфиденциальности
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),  # Условия использования
    # path('gift-certificate/create/', views.gift_certificate_create, name='gift_certificate_create'),  # Подарочные сертификаты
    path('gallery/', views.gallery, name='gallery'),  # Галерея
    path('apply/', views.application_view, name='application'),  # Форма заявки
    path('apply/success/', views.application_success, name='application_success'),  # Успешная заявка
    path('event/create/', views.event_create, name='event_create'),  # Создание мероприятия
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Детали мероприятия
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),  # Детали оборудования
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
