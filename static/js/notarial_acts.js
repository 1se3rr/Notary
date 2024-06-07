document.addEventListener('DOMContentLoaded', function() {
    // Функция для обновления списка действий выбранной категории
    function updateActionsList(categoryId) {
        // Получаем данные категорий через API
        fetch(`/api/categories`)
            .then(response => response.json())
            .then(categories => {
                // Находим выбранную категорию по ID
                const selectedCategory = categories.find(cat => cat.id === parseInt(categoryId));

                // Очищаем список действий перед обновлением
                actionsList.innerHTML = '';

                // Добавляем действия выбранной категории в список
                selectedCategory.actions.forEach(action => {
                    const actionDiv = document.createElement('div');
                    actionDiv.className = 'action-item';
                    actionDiv.innerHTML = `<strong>${action.name}</strong>`;

                    const descriptionDiv = document.createElement('div');
                    descriptionDiv.className = 'action-description';
                    descriptionDiv.innerHTML = `${action.description}`;
                    descriptionDiv.style.display = 'none';  // Скрыть описание по умолчанию

                    // Добавляем описание как дочерний элемент к действию
                    actionDiv.appendChild(descriptionDiv);

                    // Добавляем обработчик события для показа/скрытия описания при клике
                    actionDiv.addEventListener('click', () => {
                        descriptionDiv.style.display = descriptionDiv.style.display === 'none' ? 'block' : 'none';
                    });

                    // Добавляем действие в список действий
                    actionsList.appendChild(actionDiv);
                });
            })
            .catch(error => {
                console.error('Ошибка загрузки категорий:', error);
            });
    }

    const categoryTabs = document.querySelectorAll('.category-tab');
    const actionsList = document.getElementById('actions-list');

    // Добавляем обработчики событий для вкладок категорий
    categoryTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const categoryId = this.getAttribute('data-category-id');
            updateActionsList(categoryId);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.category-tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
