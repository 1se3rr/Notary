document.addEventListener('DOMContentLoaded', function () {
    // Функция для обновления размеров шрифтов
    function updateFontSizes() {
        const isMobile = window.innerWidth < 768;
        const elements = [

        ];

        elements.forEach(element => {
            document.querySelectorAll(element.selector).forEach(el => {
                el.style.fontSize = isMobile ? element.mobileSize : element.desktopSize;
            });
        });
    }

    // Функция для загрузки категорий
    function loadCategories() {
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
    }

    // Вызов функций при загрузке страницы
    updateFontSizes();
    loadCategories();

    // Добавление обработчика изменения размера окна
    window.addEventListener('resize', updateFontSizes);
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tariffs')
        .then(response => response.json())
        .then(data => {
            const titlesListLeft = document.getElementById('titles-list-left');
            const titlesListRight = document.getElementById('titles-list-right');
            data.forEach((title, index) => {
                const listItem = document.createElement('li');

                const image = document.createElement('img');
                image.src = 'static/img/point.png';
                image.alt = 'Category Image';

                const text = document.createTextNode(` ${title.title}`);

                listItem.appendChild(image);
                listItem.appendChild(text);

                if (index % 2 === 0) {
                    titlesListLeft.appendChild(listItem);
                } else {
                    titlesListRight.appendChild(listItem);
                }
            });
        })
        .catch(error => console.error('Ошибка загрузки данных заголовков:', error));
});
;



