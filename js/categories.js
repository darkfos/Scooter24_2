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
         let favorites = [];
         let cart = [];
 
         function updateFavoriteCount() {
             document.getElementById('favorite-count').textContent = favorites.length;
         }
 
         function updateCartCount() {
             document.getElementById('cart-count').textContent = cart.reduce((acc, item) => acc + item.quantity, 0);
         }
 
         function addToFavorites(product) {
             const exists = favorites.some(fav => fav.title === product.title);
             if (!exists) {
                 favorites.push(product);
                 updateFavoriteCount();
             }
         }
 
         function addToCart(product) {
             const existingProduct = cart.find(item => item.title === product.title);
             if (existingProduct) {
                 existingProduct.quantity += 1;
             } else {
                 product.quantity = 1;
                 cart.push(product);
             }
             updateCartCount();
         }
 
         function removeFromFavorites(productTitle) {
             favorites = favorites.filter(fav => fav.title !== productTitle);
             updateFavoriteCount();
             renderFavorites();
         }
 
         function removeFromCart(productTitle) {
             const existingProduct = cart.find(item => item.title === productTitle);
             if (existingProduct.quantity > 1) {
                 existingProduct.quantity -= 1;
             } else {
                 cart = cart.filter(item => item.title !== productTitle);
             }
             updateCartCount();
             renderCart();
         }
 
         function buyItems() {
             alert('Покупка совершена!');
             cart = [];
             updateCartCount();
         }
 
         document.addEventListener('DOMContentLoaded', () => {
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
                         <button onclick="removeFromFavorites('${product.title}')">Удалить</button>
                         <button onclick="addFavoriteToCart('${product.title}')">В корзину</button>
                     </td>
                 `;
             });
         }
 
         function addFavoriteToCart(productTitle) {
             const product = favorites.find(item => item.title === productTitle);
             if (product) {
                 addToCart(product);
                 removeFromFavorites(productTitle);
             }
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
                     <td><button onclick="removeFromCart('${product.title}')">Удалить</button></td>
                 `;
             });
             document.getElementById('total-price').textContent = `$${cart.reduce((acc, product) => acc + parseFloat(product.price) * product.quantity, 0).toFixed(2)}`;
         }
 
         function increaseQuantity(productTitle) {
             const existingProduct = cart.find(item => item.title === productTitle);
             if (existingProduct) {
                 existingProduct.quantity += 1;
                 updateCartCount();
                 renderCart();
             }
         }
 
         function decreaseQuantity(productTitle) {
             const existingProduct = cart.find(item => item.title === productTitle);
             if (existingProduct && existingProduct.quantity > 1) {
                 existingProduct.quantity -= 1;
                 updateCartCount();
                 renderCart();
             }
         }
 
         function filterProducts() {
             const minPrice = parseFloat(document.getElementById('price-filter-min').value) || 0;
             const maxPrice = parseFloat(document.getElementById('price-filter-max').value) || Infinity;
             const cards = document.querySelectorAll('.card');
 
             cards.forEach(card => {
                 const price = parseFloat(card.dataset.price);
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
                 sortedCards = cards.sort((a, b) => parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
             } else if (sortBy === 'price-desc') {
                 sortedCards = cards.sort((a, b) => parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
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
            const rowsPerPage = 2; // 2 ряда на странице
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

            function setupPagination() {
                const totalPages = Math.ceil(cards.length / (rowsPerPage * cardsPerRow));
                const prevButton = document.getElementById('prev-page');
                const nextButton = document.getElementById('next-page');

                prevButton.disabled = currentPage === 1;
                nextButton.disabled = currentPage === totalPages;

                prevButton.addEventListener('click', () => {
                    if (currentPage > 1) {
                        currentPage--;
                        displayCards();
                        setupPagination(); // Обновляем кнопки после изменения страницы
                    }
                });

                nextButton.addEventListener('click', () => {
                    if (currentPage < totalPages) {
                        currentPage++;
                        displayCards();
                        setupPagination(); // Обновляем кнопки после изменения страницы
                    }
                });
            }

            displayCards();
            setupPagination();
        });
