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
                    const titleHeader = document.createElement('h3');
                    titleHeader.textContent = titleData.title;
                    titleDiv.appendChild(titleHeader);

                    titleData.services.forEach(service => {
                        const serviceDiv = document.createElement('div');
                        serviceDiv.classList.add('service-block');
                        const serviceHeader = document.createElement('h4');
                        serviceHeader.textContent = `Сервис: ${service.name} (Норма: ${service.norm})`;
                        serviceDiv.appendChild(serviceHeader);

                        service.tariffs.forEach(tariff => {
                            const tariffDiv = document.createElement('div');
                            tariffDiv.classList.add('tariff-block');
                            tariffDiv.innerHTML = `<strong>Тип:</strong> ${tariff.type} <br>
                                                   <strong>Цена:</strong> ${tariff.price} <br>
                                                   <strong>Описание:</strong> ${tariff.description}`;
                            serviceDiv.appendChild(tariffDiv);
                        });

                        titleDiv.appendChild(serviceDiv);
                    });

                    container.appendChild(titleDiv);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки данных:', error);
            const container = document.getElementById('tariffs-container');
            container.innerHTML = '<p>Ошибка загрузки данных.</p>';
        });
});
