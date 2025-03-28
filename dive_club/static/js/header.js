// Получаем элементы
const menuToggle = document.getElementById('navbar-toggle');
const dropdownMenu = document.getElementById('navbar-menu');

// Обработчик клика по кнопке-гамбургеру
menuToggle.addEventListener('click', () => {
    dropdownMenu.classList.toggle('show'); // Переключаем класс show для меню
    document.body.classList.toggle('menu-open'); // Блокируем скролл при открытом меню
});

// Закрытие меню при клике на ссылку
dropdownMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        dropdownMenu.classList.remove('show'); // Убираем класс show
        document.body.classList.remove('menu-open'); // Сбрасываем блокировку скролла
    });
});

// Закрытие меню при клике вне меню
document.addEventListener('click', (event) => {
    if (!menuToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.remove('show'); // Убираем класс show
        document.body.classList.remove('menu-open'); // Сбрасываем блокировку скролла
    }
});
