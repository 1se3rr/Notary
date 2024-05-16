document.addEventListener("DOMContentLoaded", function () {
    function updateFontSizes() {
        const isMobile = window.innerWidth < 768;

        // Изменение размера шрифта для всех элементов h1
        const h1s = document.querySelectorAll("h1");
        h1s.forEach(h1 => {
            h1.style.fontSize = isMobile ? "24px" : "48px";
        });

        // Изменение размера шрифта для всех элементов h2
        const h2s = document.querySelectorAll("h2");
        h2s.forEach(h2 => {
            h2.style.fontSize = isMobile ? "20px" : "32px";
        });
    }

    // Вызов функции при загрузке страницы
    updateFontSizes();

    // Добавление обработчика изменения размера окна
    window.addEventListener("resize", updateFontSizes);
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/categories')
        .then(response => response.json())
        .then(categories => {
            const categoriesListLeft = document.getElementById('categories-list-left');
            const categoriesListRight = document.getElementById('categories-list-right');
            categories.forEach((category, index) => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<img src="static/img/point.png" alt="Category Image"> ${category.name}`;
                if (index % 2 === 0) {  // Распределение категорий по колонкам
                    categoriesListLeft.appendChild(listItem);
                } else {
                    categoriesListRight.appendChild(listItem);
                }
            });
        })
        .catch(error => console.error('Ошибка загрузки категорий:', error));
});




