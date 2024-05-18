document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tariffs')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const container = document.getElementById('tariffs-container');
            if (data.length === 0) {
                container.innerHTML = '<p>Тарифы не найдены.</p>';
            } else {
                data.forEach(titleData => {
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
                        const serviceDiv = document.createElement('div');
                        serviceDiv.classList.add('service-block');
                        serviceDiv.setAttribute('data-service-id', service.name);
                        const serviceHeader = document.createElement('button');
                        serviceHeader.classList.add('service-button');
                        serviceHeader.textContent = service.name;
                        serviceDiv.appendChild(serviceHeader);

                        servicesList.appendChild(serviceDiv);
                    });

                    titleDiv.appendChild(servicesList);
                    container.appendChild(titleDiv);

                    titleHeader.addEventListener('click', function() {
                        const servicesList = this.nextElementSibling;
                        servicesList.style.display = servicesList.style.display === 'none' ? 'grid' : 'none';
                    });
                });

                // Обработчик для кнопок сервисов
                document.querySelectorAll('.service-button').forEach(button => {
                    button.addEventListener('click', function() {
                        const serviceName = this.parentElement.getAttribute('data-service-id');
                        const titleName = this.closest('.title-block').getAttribute('data-title-id');
                        const serviceData = data.find(title => title.title === titleName).services.find(service => service.name === serviceName);

                        console.log('Service Data:', serviceData); // Отладочное сообщение для проверки данных сервиса

                        if (serviceData && serviceData.tariffs) {
                            // Сортировка тарифов по типу
                            const federalTariffs = serviceData.tariffs.filter(tariff => tariff.type.includes('Федеральный'));
                            const regionalTariffs = serviceData.tariffs.filter(tariff => tariff.type.includes('Региональный'));

                            console.log('Federal Tariffs:', federalTariffs); // Отладочное сообщение для проверки федеральных тарифов
                            console.log('Regional Tariffs:', regionalTariffs); // Отладочное сообщение для проверки региональных тарифов

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
                        } else {
                            console.error('Тарифы не найдены для сервиса:', serviceName);
                        }
                    });
                });
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки данных:', error);
            const container = document.getElementById('tariffs-container');
            container.innerHTML = '<p>Ошибка загрузки данных.</p>';
        });

    // Закрытие модального окна
    const modal = document.getElementById('modal');
    const span = document.getElementsByClassName('close')[0];

    span.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
});
