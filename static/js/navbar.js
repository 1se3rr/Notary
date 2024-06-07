 function toggleMenu() {
            console.log("Toggle menu function called"); // Отладочное сообщение
            const menu = document.querySelector('header nav ul');
            menu.classList.toggle('show');
        }

        document.addEventListener('DOMContentLoaded', (event) => {
            console.log("DOM fully loaded and parsed");
        });