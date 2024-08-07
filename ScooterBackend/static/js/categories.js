//поиск
var lastResFind = ""; // последний удачный результат
var copy_page = ""; // копия страницы в исходном виде

function TrimStr(s) {
    s = s.replace(/^\s+/g, '');
    return s.replace(/\s+$/g, '');
}

function FindOnPage(inputId) { //ищет текст на странице, в параметр передается ID поля для ввода
    var obj = window.document.getElementById(inputId);
    var textToFind;

    if (obj) {
        textToFind = TrimStr(obj.value); //обрезаем пробелы
    } else {
        alert("Введенная фраза не найдена");
        return;
    }
    if (textToFind == "") {
        alert("Вы ничего не ввели");
        return;
    }

    var pattern = new RegExp(textToFind, "gi");

    if (!pattern.test(document.body.innerHTML)) {
        alert("Ничего не найдено, проверьте правильность ввода!");
        return;
    }

    if (copy_page.length > 0) {
        document.body.innerHTML = copy_page;
    } else {
        copy_page = document.body.innerHTML;
    }

    document.body.innerHTML = document.body.innerHTML.replace(eval("/name=" + lastResFind + "/gi"), " "); //стираем предыдущие якори для скрола
    document.body.innerHTML = document.body.innerHTML.replace(pattern, "<a class='highlighted' name=" + textToFind + ">" + textToFind + "</a>"); //Заменяем найденный текст ссылками с якорем;
    lastResFind = textToFind; // сохраняем фразу для поиска, чтобы в дальнейшем по ней стереть все ссылки

    // Найти элемент с именем, соответствующим найденному тексту, и прокрутить его в видимую область
    var targetElement = document.querySelector("[name='" + textToFind + "']");
    if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}


  //меню
  function toggleMenu() {
    var submenu = document.querySelector('.submenu');
    submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
}

//избранное на карточке
function toggleFavorite(button) {
  button.classList.toggle('favorited');
}


//шапка сворачивается при отпределенном количестве прокрутки, позже доделать
let prevScrollPos = window.pageYOffset;
let isMenuOpen = false; // Флаг для отслеживания состояния меню

function scrollHandler(event) {
    const currentScrollPos = window.pageYOffset;
    const header = document.getElementById("header");
    const actionContainer = document.querySelector(".action-container");
    const submenu = document.querySelector('.submenu');

    if (currentScrollPos < 100) {
        // Если мы находимся в верхней части страницы
        header.style.height = "100px"; /* Показываем шапку */
        actionContainer.style.marginLeft = "0"; // Вернуть обычный margin-left
        if (isMenuOpen) {
            submenu.style.display = 'block'; // Показ подменю
            setTimeout(() => submenu.style.opacity = "1", 0); // Показать текст
        }
    } else {
        header.style.height = "50px"; /* Скрываем верхнюю часть шапки при прокрутке вниз */
        submenu.style.opacity = '0'; // Скрыть текст
        setTimeout(() => submenu.style.display = 'none', 500); // Скрыть подменю после плавного перехода
        actionContainer.style.marginLeft = "-7px"; 
        isMenuOpen = false; // Сбрасываем флаг меню
    }
    
    prevScrollPos = currentScrollPos;
}

function toggleMenu() {
    const header = document.querySelector('.header');
    const submenu = document.querySelector('.submenu');
    const logoText = document.querySelector('.logo-text');

    // Если шапка свернута, развернуть её
    if (!isMenuOpen && window.pageYOffset < 100) {
        header.style.height = '100px'; // Вернуть обычную высоту
        submenu.style.display = 'block'; // Показ подменю
        setTimeout(() => submenu.style.opacity = "1", 0); // Показать текст
        isMenuOpen = true;
    } else {
        // Иначе, свернуть шапку и скрыть подменю
        header.style.height = '50px';
        submenu.style.opacity = '0'; // Скрыть текст
        setTimeout(() => submenu.style.display = 'none', 500); // Скрыть подменю после плавного перехода
        isMenuOpen = false;
    }
}

// Добавляем обработчики событий
window.addEventListener('scroll', scrollHandler);
// document.getElementById('menu-toggle-button').addEventListener('click', toggleMenu);






//корзина, избранное и фильтры
         // Массив для хранения избранных товаров
//корзина, избранное и фильтры
         // Массив для хранения избранных товаров
// Инициализация корзины и избранного из localStorage
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Обновление счетчиков
function updateFavoriteCount() {
    document.getElementById('favorite-count').textContent = favorites.length;
}

function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.reduce((acc, item) => acc + item.quantity, 0);
}

// Сохранение данных в localStorage
function saveFavorites() {
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Преобразование цены в число
function parsePrice(price) {
    return parseFloat(price.replace('руб.', '').replace('₽', '').replace(',', '.'));
}

// Форматирование цены в рублях
function formatPrice(price) {
    return `${price.toFixed(2).replace('.', ',')} ₽`;
}

// Добавление и удаление товаров из избранного
function addToFavorites(product) {
    if (!favorites.some(fav => fav.title === product.title)) {
        favorites.push(product);
        saveFavorites();
        updateFavoriteCount();
    }
}

function removeFromFavorites(productTitle) {
    favorites = favorites.filter(fav => fav.title !== productTitle);
    saveFavorites();
    updateFavoriteCount();
    renderFavorites();
}

// Добавление и удаление товаров из корзины
function addToCart(product) {
    const existingProduct = cart.find(item => item.title === product.title);
    if (existingProduct) {
        existingProduct.quantity += 1;
    } else {
        product.quantity = 1;
        cart.push(product);
    }
    saveCart();
    updateCartCount();
}

function removeFromCart(productTitle) {
    const existingProduct = cart.find(item => item.title === productTitle);
    if (existingProduct.quantity > 1) {
        existingProduct.quantity -= 1;
    } else {
        cart = cart.filter(item => item.title !== productTitle);
    }
    saveCart();
    updateCartCount();
    renderCart();
}

// Отображение корзины и избранного
function renderFavorites() {
    const favoriteList = document.getElementById('favorite-list').getElementsByTagName('tbody')[0];
    favoriteList.innerHTML = '';
    favorites.forEach(product => {
        const row = favoriteList.insertRow();
        row.innerHTML = `
            <td><img src="${product.image}" alt="${product.title}" width="50"></td>
            <td>${product.title}</td>
            <td>${product.price}</td>
            <td>${product.availability}</td>
            <td>
                <button class = "add-to-cart" onclick="addFavoriteToCart('${product.title}')">Добавить в корзину</button>
                <button class ="remove-from-favorites" onclick="removeFromFavorites('${product.title}')">Удалить</button> 
            </td>
        `;
    });
}

function renderCart() {
    const cartList = document.getElementById('cart-list').getElementsByTagName('tbody')[0];
    cartList.innerHTML = '';
    cart.forEach(product => {
        const row = cartList.insertRow();
        row.innerHTML = `
            <td><img src="${product.image}" alt="${product.title}" width="50"></td>
            <td>${product.title}</td>
            <td>${product.price}</td>
            <td>
                <button onclick="decreaseQuantity('${product.title}')">-</button>
                ${product.quantity}
                <button onclick="increaseQuantity('${product.title}')">+</button>
            </td>
           <td><button class="remove-button" onclick="removeFromCart('${product.title}')">Удалить</button></td>
        `;
    });
    document.getElementById('total-price').textContent = formatPrice(cart.reduce((acc, product) => acc + parsePrice(product.price) * product.quantity, 0));
}

// Обработка увеличения и уменьшения количества товаров
function increaseQuantity(productTitle) {
    const existingProduct = cart.find(item => item.title === productTitle);
    if (existingProduct) {
        existingProduct.quantity += 1;
        saveCart();
        updateCartCount();
        renderCart();
    }
}

function decreaseQuantity(productTitle) {
    const existingProduct = cart.find(item => item.title === productTitle);
    if (existingProduct && existingProduct.quantity > 1) {
        existingProduct.quantity -= 1;
        saveCart();
        updateCartCount();
        renderCart();
    }
}

// Обработка покупки товаров
function buyItems() {
    alert('Покупка совершена!');
    cart = [];
    saveCart();
    updateCartCount();
    renderCart();
}

// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
    updateFavoriteCount();
    updateCartCount();
    renderFavorites();
    renderCart();

    const favoriteButtons = document.querySelectorAll('.favorite-button');
    const addToCartButtons = document.querySelectorAll('.add-to-cart-button');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const card = event.target.closest('.card');
            const product = {
                title: card.querySelector('h3').textContent,
                price: card.querySelector('.price').textContent,
                availability: card.querySelector('.availability').textContent,
                image: card.querySelector('img').src
            };
            addToFavorites(product);
        });
    });

    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const card = event.target.closest('.card');
            const product = {
                title: card.querySelector('h3').textContent,
                price: card.querySelector('.price').textContent,
                availability: card.querySelector('.availability').textContent,
                image: card.querySelector('img').src
            };
            addToCart(product);
        });
    });

    const favoriteButton = document.getElementById('favorite-button');
    const favoritesModal = document.getElementById('favorites-modal');
    const favoritesClose = document.getElementById('favorites-close');

    favoriteButton.addEventListener('click', () => {
        renderFavorites();
        favoritesModal.style.display = 'block';
    });

    favoritesClose.addEventListener('click', () => {
        favoritesModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === favoritesModal) {
            favoritesModal.style.display = 'none';
        }
    });

    const cartButton = document.getElementById('cart-button');
    const cartModal = document.getElementById('cart-modal');
    const cartClose = document.querySelector('#cart-modal .close');

    cartButton.addEventListener('click', () => {
        renderCart();
        cartModal.style.display = 'block';
    });

    cartClose.addEventListener('click', () => {
        cartModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === cartModal) {
            cartModal.style.display = 'none';
        }
    });
});

// Фильтрация и сортировка товаров
function filterProducts() {
    const minPrice = parseFloat(document.getElementById('price-filter-min').value) || 0;
    const maxPrice = parseFloat(document.getElementById('price-filter-max').value) || Infinity;
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        const price = parsePrice(card.dataset.price);
        if (price >= minPrice && price <= maxPrice) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function sortProducts() {
    const sortBy = document.getElementById('sorting').value;
    const cardsContainer = document.querySelector('.cards-container');
    const cards = Array.from(cardsContainer.children);

    let sortedCards;
    if (sortBy === 'price-asc') {
        sortedCards = cards.sort((a, b) => parsePrice(a.dataset.price) - parsePrice(b.dataset.price));
    } else if (sortBy === 'price-desc') {
        sortedCards = cards.sort((a, b) => parsePrice(b.dataset.price) - parsePrice(a.dataset.price));
    } else if (sortBy === 'availability') {
        sortedCards = cards.sort((a, b) => parseInt(b.dataset.availability) - parseInt(a.dataset.availability));
    } else {
        sortedCards = cards;
    }

    cardsContainer.innerHTML = '';
    sortedCards.forEach(card => cardsContainer.appendChild(card));
}

function resetPriceFilter() {
    document.getElementById('price-filter-min').value = '';
    document.getElementById('price-filter-max').value = '';
    filterProducts();
}

function resetSorting() {
    document.getElementById('sorting').value = 'default';
    sortProducts();
}






//навигация
document.addEventListener('DOMContentLoaded', function() {
    const cardsPerRow = 4; // 4 карточки в каждом ряду
    const rowsPerPage = 3; // 2 ряда на странице (всего 8 карточек)
    const cardsContainer = document.getElementById('cards-container');
    const cards = Array.from(cardsContainer.getElementsByClassName('card'));
    let currentPage = 1;

    function displayCards() {
        const startIndex = (currentPage - 1) * rowsPerPage * cardsPerRow;
        const endIndex = Math.min(startIndex + rowsPerPage * cardsPerRow, cards.length);

        cards.forEach((card, index) => {
            card.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
        });
    }

    function updatePaginationButtons() {
        const totalPages = Math.ceil(cards.length / (rowsPerPage * cardsPerRow));
        const prevButton = document.getElementById('prev-page');
        const nextButton = document.getElementById('next-page');

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }

    function setupPagination() {
        const prevButton = document.getElementById('prev-page');
        const nextButton = document.getElementById('next-page');

        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                displayCards();
                updatePaginationButtons(); // Обновляем кнопки после изменения страницы
            }
        });

        nextButton.addEventListener('click', () => {
            const totalPages = Math.ceil(cards.length / (rowsPerPage * cardsPerRow));
            if (currentPage < totalPages) {
                currentPage++;
                displayCards();
                updatePaginationButtons(); // Обновляем кнопки после изменения страницы
            }
        });
    }

    displayCards();
    setupPagination();
    updatePaginationButtons(); // Устанавливаем начальное состояние кнопок
});

        // Отображение модального окна
function showModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'block';
  }
  
// Отображение модального окна
function showModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'block';
  }
  
  // Закрытие модального окна при клике вне его
  window.onclick = function(event) {
    const modal = document.getElementById('myModal');
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  }
  
  // Закрытие модального окна при клике на крестик
  function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
  }
  
  // Переадресация на WhatsApp
  function redirectToWhatsApp() {
    window.location.href = 'https://wa.me/номер_WhatsApp';
  }
  
  // Переадресация на Telegram
  function redirectToTelegram() {
    window.location.href = 'https://t.me/Calm_the_loony';
  }
  
  // Инициирование звонка
  function makePhoneCall() {
    window.location.href = 'tel:+9614277510';
  }
  


  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function() {
            const product = {
                image: this.querySelector('img').src,
                name: this.querySelector('h3').innerText,
                description: this.querySelector('.description').innerText,
                price: this.dataset.price,
                availability: this.dataset.availability
            };
            localStorage.setItem('selectedProduct', JSON.stringify(product));
            window.location.href = 'product.html';
        });
    });
});