document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("gallery-modal");
    const closeModal = document.querySelector(".close-modal");
    const gallerySlider = document.querySelector(".gallery-slider");
    const galleryText = document.querySelector(".gallery-text");

    // Обработчик клика на карточку мероприятия
    document.querySelectorAll(".event-card").forEach(card => {
        card.addEventListener("click", function () {
            const eventId = this.dataset.eventId;

            // Переход на страницу мероприятия
            window.location.href = `/event/${eventId}/`; // Замените на ваш URL
        });
    });

    // Закрытие модального окна
    closeModal.addEventListener("click", function () {
        modal.style.display = "none"; // Скрываем модальное окно
        removeNavigationButtons(); // Удаляем кнопки навигации
    });

    // Закрытие модального окна при клике вне его
    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none"; // Скрываем модальное окно
            removeNavigationButtons(); // Удаляем кнопки навигации
        }
    });

    function removeNavigationButtons() {
        document.querySelectorAll(".prev, .next").forEach(button => button.remove()); // Удаляем кнопки навигации
    }
});
