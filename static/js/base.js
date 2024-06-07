function handleScroll() {
    const boxes = document.querySelectorAll('.description , .license-number, .actions-section, .tariffs-section, .faq-link, .gos-link ');
    const isMobile = window.innerWidth < 893;

    if (isMobile) {
        boxes.forEach(box => {
            const boxTop = box.getBoundingClientRect().top;
            const boxBottom = box.getBoundingClientRect().bottom;
            const windowHeight = window.innerHeight;

            if (boxTop < windowHeight / 2 && boxBottom > windowHeight / 2) {
                box.classList.add('scroll-lift');
            } else {
                box.classList.remove('scroll-lift');
            }
        });
    } else {
        boxes.forEach(box => {
            box.classList.remove('scroll-lift');
        });
    }
}

// Добавляем обработчик события прокрутки
window.addEventListener('scroll', handleScroll);
// Вызываем функцию один раз при загрузке страницы
handleScroll();

// Добавляем обработчик изменения размера окна, чтобы учитывать изменение ширины экрана
window.addEventListener('resize', handleScroll);
