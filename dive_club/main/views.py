from django.shortcuts import render, redirect
from .models import HomePageContent, Event, EventImage, EquipmentPageContent, GalleryImage


def home(request):
    homepage_content = HomePageContent.objects.first()  # Предполагаем, что объект один
    instructor = homepage_content.instructor if homepage_content else None
    events = homepage_content.events.all() if homepage_content else []  # Изменяем для получения событий

    context = {
        'homepage_content': homepage_content,
        'instructor': instructor,
        'discount_title': homepage_content.discount_title if homepage_content else None,
        'discount_description': homepage_content.discount_description if homepage_content else None,
        'discount_percentage': homepage_content.discount_percentage if homepage_content else None,
        'instructor_room_photo': instructor.room_photo.url if instructor and instructor.room_photo else None,
        'events': events,
    }
    return render(request, 'main/home.html', context)

def gift_certificate_create(request):
    if request.method == 'POST':
        tg_id = request.POST.get('tg_id')
        if tg_id:  # Проверяем, что tg_id не пустой
            homepage_content = HomePageContent.objects.first()
            if homepage_content:  # Проверяем, что объект существует
                homepage_content.tg_id = tg_id
                homepage_content.save()
                return redirect('homepage')  # Перенаправление на главную страницу после успешного сохранения
    return render(request, 'your_template.html')

def about(request):
    return render(request, 'about.html')

def training(request):
    return render(request, 'training.html')


def equipment(request):
    # Предполагается, что EquipmentPageContent существует в единственном экземпляре
    equipment_page_content = EquipmentPageContent.objects.first()
    # Получаем список оборудования, связанного с этой страницей
    equipment_list = equipment_page_content.equipment.all() if equipment_page_content else []

    context = {
        'equipment_page_content': equipment_page_content,
        'equipment_list': equipment_list,
    }
    return render(request, 'main/equipment.html', context)

def contacts(request):
    return render(request, 'contacts.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')


def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        homepage_content = HomePageContent.objects.first()  # Получение первого объекта HomePageContent
        event = Event.objects.create(title=title, description=description, homepage_content=homepage_content)

        # Обработка изображений
        images = request.FILES.getlist('images')
        for image in images:
            EventImage.objects.create(event=event, image=image)

        return redirect('some_view')  # перенаправление после создания

    return render(request, 'event_create.html')  # шаблон для создания мероприятия



def gallery(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')  # Сортировка от новых к старым
    return render(request, 'main/gallery.html', {'images': images})