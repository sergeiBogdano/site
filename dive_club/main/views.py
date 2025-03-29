from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    HomePageContent, Event, EventImage, EquipmentPageContent,
    GalleryImage, TrainingPage, AboutPage, ContactPage, TermsOfService,
    PrivacyPolicy, Equipment, EquipmentCategory, TrainingCourse
)
from .forms import ApplicationForm
from django.http import JsonResponse


def home(request):
    """Главная страница."""
    homepage_content = HomePageContent.objects.first()
    context = {
        'homepage_content': homepage_content,
        'instructor': homepage_content.instructor if homepage_content else None,
        'discount_title': homepage_content.discount_title if homepage_content else None,
        'discount_description': homepage_content.discount_description if homepage_content else None,
        'discount_percentage': homepage_content.discount_percentage if homepage_content else None,
        'original_price': homepage_content.original_price if homepage_content else None,
        'discounted_price': homepage_content.discounted_price if homepage_content else None,
        'instructor_room_photo': (
            homepage_content.instructor.room_photo.url
            if homepage_content and homepage_content.instructor and
            homepage_content.instructor.room_photo else None
        ),
        'events': homepage_content.events.all() if homepage_content else [],
    }
    return render(request, 'home/home.html', context)


def about(request):
    """Страница 'О нас'."""
    about_page = AboutPage.objects.first()
    instructors = about_page.instructors.all() if about_page else []
    context = {
        'about_page': about_page,
        'instructors': instructors,
    }
    return render(request, 'about/about.html', context)


def training(request):
    """Страница обучения с курсами, изображениями и видео."""
    training_page = TrainingPage.objects.prefetch_related("courses__images", "courses__videos").first()

    # Получаем уникальные категории курсов
    categories = TrainingCourse.objects.values_list("course_category", flat=True).distinct()

    return render(request, "training/training.html", {
        "training": training_page,
        "categories": categories  # Передаем в шаблон
    })


def course_detail(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    return render(request, "training/course_detail.html", {"course": course})


def equipment_list(request):
    """Страница ремонта оборудования."""
    equipment_page_content = EquipmentPageContent.objects.first()
    equipment_categories = EquipmentCategory.objects.all()

    category_name = request.GET.get('category')
    if category_name:
        equipment_list = Equipment.objects.filter(category__name=category_name)
    else:
        equipment_list = Equipment.objects.all()

    context = {
        'equipment_list': equipment_list,
        'equipment_page_content': equipment_page_content,
        'equipment_categories': equipment_categories,
        'selected_category': category_name,
    }
    return render(request, 'equipment/equipment_list.html', context)


def equipment_detail(request, pk):
    """Детальная страница ремонта оборудования."""
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'equipment/equipment_detail.html', {'equipment': equipment})


def contacts(request):
    """Страница контактов."""
    contact_info = ContactPage.objects.first()
    return render(request, 'contacts/contacts.html', {'contact_info': contact_info})


def terms_of_service(request):
    """Условия использования."""
    terms = TermsOfService.objects.first()
    return render(request, 'main/terms_of_policy.html', {'terms': terms})


def privacy_policy(request):
    """Политика конфиденциальности."""
    policy = PrivacyPolicy.objects.first()
    return render(request, 'main/policy.html', {'policy': policy})


def event_create(request):
    """Создание мероприятия."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')
        homepage_content = HomePageContent.objects.first()
        event = Event.objects.create(title=title, description=description)
        event.homepage_content.add(homepage_content)

        EventImage.objects.bulk_create([
            EventImage(event=event, image=image) for image in images
        ])

        return redirect('home')
    return render(request, 'events/event_create.html')


def event_detail(request, event_id):
    """Детальная страница мероприятия."""
    event = get_object_or_404(Event, id=event_id)
    images = [img.image.url for img in event.images.all()]
    context = {
        'event': event,
        'images': images,
    }
    return render(request, 'events/event_detail.html', context)


def gallery(request):
    """Галерея изображений."""
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery/gallery.html', {'images': images})


def application_view(request):
    """Форма заявки."""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Ваша заявка успешно отправлена!'
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ApplicationForm()
    return render(request, 'application/application.html', {'form': form})


def application_success(request):
    """Успешная заявка."""
    return render(request, 'application/application_success.html')
