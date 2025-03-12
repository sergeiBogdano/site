from django.shortcuts import render, redirect
from .models import HomePageContent  # Предполагаем, что вы работаете с этой моделью


def home(request):
    homepage_content = HomePageContent.objects.first()  # Предполагаем, что объект один
    context = {
        'homepage_content': homepage_content,
        'instructor': homepage_content.instructor if homepage_content else None,
        'diver_model': homepage_content.diver_model_link if homepage_content else None,
        'discount_title': homepage_content.discount_title if homepage_content else None,
        'discount_description': homepage_content.discount_description if homepage_content else None,
        'discount_percentage': homepage_content.discount_percentage if homepage_content else None,
    }
    return render(request, 'main/home.html', context)


def gift_certificate_create(request):
    if request.method == 'POST':
        tg_id = request.POST.get('tg_id')
        # Сохранение Telegram ID в модели HomePageContent
        homepage_content = HomePageContent.objects.first()  # Получаем первый объект (или используйте другой способ)
        homepage_content.tg_id = tg_id
        homepage_content.save()
        return redirect('homepage')  # Перенаправление на главную страницу после успешного сохранения
    return render(request, 'your_template.html')


def about(request):
    return render(request, 'about.html')  # Шаблон для страницы "О нас"


def training(request):
    return render(request, 'training.html')  # Шаблон для страницы "Обучение"


def equipment(request):
    return render(request, 'equipment.html')  # Шаблон для страницы "Оборудование"


def contacts(request):
    return render(request, 'contacts.html')  # Шаблон для страницы "Контакты"


def privacy_policy(request):
    return render(request, 'privacy_policy.html')  # Шаблон для страницы "Политика конфиденциальности"


def terms_of_service(request):
    return render(request, 'terms_of_service.html')  # Шаблон для страницы "Условия использования"