document.addEventListener('DOMContentLoaded', function() {
    // Функция для загрузки тарифов
    function loadTariffs() {
        fetch('/api/tariffs')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                displayTariffs(data);
            })
            .catch(error => {
                console.error('Ошибка загрузки данных:', error);
                const container = document.getElementById('tariffs-container');
                container.innerHTML = '<p>Ошибка загрузки данных.</p>';
            });
    }

    // Функция для отображения тарифов
    function displayTariffs(data) {
        const container = document.getElementById('tariffs-container');
        if (data.length === 0) {
            container.innerHTML = '<p>Тарифы не найдены.</p>';
        } else {
            data.forEach(titleData => {
                const titleDiv = createTitleBlock(titleData);
                container.appendChild(titleDiv);
            });

            // Добавление обработчиков для кнопок сервисов
            document.querySelectorAll('.service-button').forEach(button => {
                button.addEventListener('click', handleServiceButtonClick);
            });
        }
    }

    // Функция для создания блока заголовка
    function createTitleBlock(titleData) {
        const titleDiv = document.createElement('div');
        titleDiv.classList.add('title-block');
        titleDiv.setAttribute('data-title-id', titleData.title);

        const titleHeader = document.createElement('button');
        titleHeader.classList.add('title-button');
        titleHeader.textContent = titleData.title;
        titleDiv.appendChild(titleHeader);

        const servicesList = document.createElement('div');
        servicesList.classList.add('services-list');
        servicesList.style.display = 'none';

        titleData.services.forEach(service => {
            const serviceDiv = createServiceBlock(service);
            servicesList.appendChild(serviceDiv);
        });

        titleDiv.appendChild(servicesList);

        titleHeader.addEventListener('click', function() {
            servicesList.style.display = servicesList.style.display === 'none' ? 'grid' : 'none';
        });

        return titleDiv;
    }

    // Функция для создания блока сервиса
    function createServiceBlock(service) {
        const serviceDiv = document.createElement('div');
        serviceDiv.classList.add('service-block');
        serviceDiv.setAttribute('data-service-id', service.name);

        const serviceHeader = document.createElement('button');
        serviceHeader.classList.add('service-button');
        serviceHeader.textContent = service.name;
        serviceDiv.appendChild(serviceHeader);

        return serviceDiv;
    }

    // Обработчик клика по кнопке сервиса
    function handleServiceButtonClick() {
        const serviceName = this.parentElement.getAttribute('data-service-id');
        const titleName = this.closest('.title-block').getAttribute('data-title-id');

        fetch('/api/tariffs')
            .then(response => response.json())
            .then(data => {
                const serviceData = data.find(title => title.title === titleName)
                                       .services.find(service => service.name === serviceName);

                if (serviceData && serviceData.tariffs) {
                    displayModal(serviceData);
                } else {
                    console.error('Тарифы не найдены для сервиса:', serviceName);
                }
            })
            .catch(error => {
                console.error('Ошибка загрузки данных сервиса:', error);
            });
    }

    // Функция для отображения модального окна с тарифами
    function displayModal(serviceData) {
        // Сортировка тарифов по типу
        const federalTariffs = serviceData.tariffs.filter(tariff => tariff.type.includes('Федеральный'));
        const regionalTariffs = serviceData.tariffs.filter(tariff => tariff.type.includes('Региональный'));

        const modalContent = document.getElementById('modal-content');
        if (modalContent) {
            modalContent.innerHTML = `
                <h2>${serviceData.name}</h2>
                <p>Норма: ${serviceData.norm}</p>
                <div class="tariffs-container">
                    <div class="tariff-column">
                        <h3>Федеральные тарифы (руб)</h3>
                        ${federalTariffs.map(tariff => `
                            <div class="tariff-block">
                                <p><strong>Цена:</strong> ${tariff.price}</p>
                                ${tariff.description ? `<p><strong>Описание:</strong> ${tariff.description}</p>` : ''}
                            </div>
                        `).join('')}
                    </div>
                    <div class="tariff-column">
                        <h3>Региональные тарифы (руб)</h3>
                        ${regionalTariffs.map(tariff => `
                            <div class="tariff-block">
                                <p><strong>Цена:</strong> ${tariff.price}</p>
                                ${tariff.description ? `<p><strong>Описание:</strong> ${tariff.description}</p>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            document.getElementById('modal').style.display = 'block';
        } else {
            console.error('Не найден элемент с id "modal-content"');
        }
    }

    // Закрытие модального окна
    const modal = document.getElementById('modal');
    const closeModalButton = document.getElementsByClassName('close')[0];

    closeModalButton.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };

    // Инициализация загрузки тарифов
    loadTariffs();
});
