from django.shortcuts import render, redirect
from .models import (
    HomePageContent, Event, EventImage, EquipmentPageContent,
    GalleryImage, TrainingPage, AboutPage, ContactPage
)


def home(request):
    homepage_content = HomePageContent.objects.first()

    context = {
        'homepage_content': homepage_content,
        'instructor': homepage_content.instructor if homepage_content else None,
        'discount_title': homepage_content.discount_title if homepage_content else None,
        'discount_description': homepage_content.discount_description if homepage_content else None,
        'discount_percentage': homepage_content.discount_percentage if homepage_content else None,
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
            if homepage_content:
                homepage_content.tg_id = tg_id
                homepage_content.save()
                return redirect('home')  # Измени на правильное имя маршрута
    return render(request, 'your_template.html')


def about(request):
    about_page = AboutPage.objects.first()
    instructors = about_page.instructors.all() if about_page else []

    context = {
        'about_page': about_page,
        'instructors': instructors,
    }

    return render(request, 'main/about.html', context)


def training(request):
    training = TrainingPage.objects.first()
    return render(request, "main/training.html", {"training": training})


def equipment(request):
    equipment_page_content = EquipmentPageContent.objects.first()

    context = {
        'equipment_page_content': equipment_page_content,
        'equipment_list': equipment_page_content.equipment.all() if equipment_page_content else [],
    }
    return render(request, 'main/equipment.html', context)


def contacts(request):
    contact_info = ContactPage.objects.first()  # Предполагаем, что объект один
    return render(request, 'main/contacts.html', {'contact_info': contact_info})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms_of_service.html')


def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')  # Получаем список загруженных файлов

        homepage_content = HomePageContent.objects.first()
        if homepage_content:  # Проверяем, что HomePageContent есть в базе
            event = Event.objects.create(title=title, description=description)
            event.homepage_content.add(homepage_content)  # Правильная связь ManyToMany

            # Создаем объекты EventImage
            EventImage.objects.bulk_create([
                EventImage(event=event, image=image) for image in images
            ])

            return redirect('home')  # Перенаправляем на главную страницу или нужный маршрут

    return render(request, 'event_create.html')


def gallery(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')  # Сортируем от новых к старым
    return render(request, 'main/gallery.html', {'images': images})
