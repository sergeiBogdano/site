document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("gallery-modal");
    const closeModal = document.querySelector(".close-modal");
    const modalImage = document.getElementById("modal-image");
    const prevButton = document.querySelector(".prev");
    const nextButton = document.querySelector(".next");
    const galleryItems = document.querySelectorAll(".gallery-item");
    let currentIndex = 0;

    // Обработчик клика на изображение в галерее
    galleryItems.forEach((item, index) => {
        item.addEventListener("click", function () {
            modal.style.display = "flex"; // Показываем модальное окно
            modalImage.src = this.dataset.full; // Устанавливаем источник изображения
            currentIndex = index; // Запоминаем текущий индекс
        });
    });

    // Закрытие модального окна
    closeModal.addEventListener("click", function () {
        modal.style.display = "none"; // Скрываем модальное окно
    });

    // Закрытие модального окна при клике вне его
    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none"; // Скрываем модальное окно
        }
    });

    // Навигация по изображениям
    prevButton.addEventListener("click", function () {
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : galleryItems.length - 1;
        modalImage.src = galleryItems[currentIndex].dataset.full;
    });

    nextButton.addEventListener("click", function () {
        currentIndex = (currentIndex < galleryItems.length - 1) ? currentIndex + 1 : 0;
        modalImage.src = galleryItems[currentIndex].dataset.full;
    });

    // Обработчик клика на карточку мероприятия (если нужно)
    document.querySelectorAll(".event-card").forEach(card => {
        card.addEventListener("click", function () {
            const eventId = this.dataset.eventId;

            // Переход на страницу мероприятия
            window.location.href = `/event/${eventId}/`; // Замените на ваш URL
        });
    });
});