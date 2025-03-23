from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    HomePageContent, Event, EventImage, EquipmentPageContent,
    GalleryImage, TrainingPage, AboutPage, ContactPage, TermsOfService,
    PrivacyPolicy, Equipment, EquipmentCategory
)
from .forms import ApplicationForm
from django.contrib import messages
from django.http import JsonResponse


def home(request):
    homepage_content = HomePageContent.objects.first()

    context = {
        'homepage_content': homepage_content,
        'instructor': homepage_content.instructor if homepage_content else None,
        'discount_title': homepage_content.discount_title if homepage_content else None,
        'discount_description': homepage_content.discount_description if homepage_content else None,
        'discount_percentage': homepage_content.discount_percentage if homepage_content else None,
        'original_price': homepage_content.original_price if homepage_content else None,  # Добавлено
        'discounted_price': homepage_content.discounted_price if homepage_content else None,  # Добавлено
        'instructor_room_photo': homepage_content.instructor.room_photo.url
            if homepage_content and homepage_content.instructor and homepage_content.instructor.room_photo
            else None,
        'events': homepage_content.events.all() if homepage_content else [],
    }
    return render(request, 'main/home.html', context)


def gift_certificate_create(request):
    if request.method == 'POST':
        tg_id = request.POST.get('tg_id')
        if tg_id:
            homepage_content = HomePageContent.objects.first()
            homepage_content.tg_id = tg_id
            homepage_content.save()
            return redirect('home')
    return render(request, 'main/gift_certificate.html')


def about(request):
    about_page = AboutPage.objects.first()
    instructors = about_page.instructors.all() if about_page else []

    context = {
        'about_page': about_page,
        'instructors': instructors,
    }

    return render(request, 'main/about.html', context)


def training(request):
    training_page = TrainingPage.objects.first()
    return render(request, "main/training.html", {"training": training_page})


def equipment(request):
    equipment_page_content = EquipmentPageContent.objects.first()

    context = {
        'equipment_page_content': equipment_page_content,
        'equipment_list': equipment_page_content.equipment.all() if equipment_page_content else [],
    }
    return render(request, 'main/equipment.html', context)


def contacts(request):
    contact_info = ContactPage.objects.first()
    return render(request, 'main/contacts.html', {'contact_info': contact_info})


def terms_of_service(request):
    terms = TermsOfService.objects.first()
    return render(request, 'main/terms_of_service.html', {'terms': terms})


def privacy_policy(request):
    policy = PrivacyPolicy.objects.first()
    return render(request, 'main/privacy_policy.html', {'policy': policy})


def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')  # Список загруженных файлов

        homepage_content = HomePageContent.objects.first()
        event = Event.objects.create(title=title, description=description)
        event.homepage_content.add(homepage_content)

        # Создаем объекты EventImage
        EventImage.objects.bulk_create([
            EventImage(event=event, image=image) for image in images
        ])

        return redirect('home')
    return render(request, 'main/event_create.html')


def gallery(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'main/gallery.html', {'images': images})


def application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Сохраняем данные формы в базу данных
            application = form.save()
            return JsonResponse({'success': True, 'message': 'Ваша заявка успешно отправлена!'})
        else:
            # Возвращаем ошибки валидации формы
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ApplicationForm()
    return render(request, 'main/application.html', {'form': form})


def application_success(request):
    return render(request, 'main/application_success.html')


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    images = [img.image.url for img in event.images.all()]  # Получаем ссылки на изображения

    context = {
        'event': event,
        'images': images,
    }
    return render(request, 'main/event_detail.html', context)


def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'main/equipment_detail.html', {'equipment': equipment})


def equipment_list(request):
    # Получаем контент страницы оборудования
    equipment_page_content = EquipmentPageContent.objects.first()

    # Получаем все оборудование
    equipment_list = Equipment.objects.all()  # Получаем все оборудование

    # Получаем все категории для фильтрации
    equipment_categories = EquipmentCategory.objects.all()

    # Проверка на наличие категории в GET-запросе
    category = request.GET.get('category')
    if category:
        # Если категория выбрана, фильтруем по ней
        equipment_list = equipment_list.filter(category__name=category)

    return render(request, 'main/equipment_list.html', {
        'equipment_list': equipment_list,
        'equipment_page_content': equipment_page_content,
        'equipment_categories': equipment_categories,  # Передаем категории в шаблон
    })