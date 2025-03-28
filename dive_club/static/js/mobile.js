// Получаем элементы
const menuToggle = document.getElementById('menu-toggle');
const dropdownMenu = document.getElementById('dropdown-menu');
const scrollToTopButton = document.querySelector('.scroll-to-top');

// Проверяем, что элементы существуют
if (menuToggle && dropdownMenu && scrollToTopButton) {
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

    // Отображение кнопки "Наверх" при прокрутке
    window.addEventListener('scroll', () => {
        if (window.scrollY > 200) {
            scrollToTopButton.classList.add('show'); // Показываем кнопку
        } else {
            scrollToTopButton.classList.remove('show'); // Скрываем кнопку
        }
    });
}
