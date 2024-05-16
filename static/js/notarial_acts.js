document.addEventListener('DOMContentLoaded', function() {
    const categoryTabs = document.querySelectorAll('.category-tab');
    const actionsList = document.getElementById('actions-list');

    categoryTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const categoryId = this.getAttribute('data-category-id');
            fetch(`/api/categories`)
                .then(response => response.json())
                .then(categories => {
                    const selectedCategory = categories.find(cat => cat.id === parseInt(categoryId));
                    actionsList.innerHTML = '';
                    selectedCategory.actions.forEach(action => {
                        const actionDiv = document.createElement('div');
                        actionDiv.className = 'action-item';
                        actionDiv.innerHTML = `<strong>${action.name}</strong>`;

                        const descriptionDiv = document.createElement('div');
                        descriptionDiv.className = 'action-description';
                        descriptionDiv.innerHTML = `${action.description}`;
                        descriptionDiv.style.display = 'none';  // Скрыть описание

                        actionDiv.appendChild(descriptionDiv);
                        actionDiv.addEventListener('click', () => {
                            descriptionDiv.style.display = descriptionDiv.style.display === 'none' ? 'block' : 'none';
                        });

                        actionsList.appendChild(actionDiv);
                    });
                });
        });
    });
});
