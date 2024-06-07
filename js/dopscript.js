//карта
document.addEventListener('DOMContentLoaded', () => {
    // Скрипты, специфичные для страницы торгового помещения
    const mapElement = document.getElementById('map');
    if (mapElement) {
      var map = L.map('map').setView([47.2313, 39.7233], 13); // Координаты для Ростова-на-Дону
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      L.marker([47.2313, 39.7233]).addTo(map)
        .bindPopup('Торговое помещение.<br> Ул. Мечникова 35')
        .openPopup();
    }
  
    // Добавьте другие специфичные скрипты для торгового помещения здесь
  });
  


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




//избранное и корзина
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
let cart = JSON.parse(localStorage.getItem('cart')) || [];

const favoriteButton = document.getElementById('favorite-button');
const favoriteCount = document.getElementById('favorite-count');
const favoriteList = document.querySelector('#favorite-list tbody');
const favoritesModal = document.getElementById('favorites-modal');
const favoritesClose = document.getElementById('favorites-close');

const cartButton = document.getElementById('cart-button');
const cartCount = document.getElementById('cart-count');
const cartList = document.querySelector('#cart-list tbody');
const cartModal = document.getElementById('cart-modal');
const cartClose = document.getElementById('cart-close');

function saveFavorites() {
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function toggleFavorite(button) {
    const productCard = button.closest('.product-card');
    const productId = productCard.getAttribute('data-id');
    const product = {
        id: productId,
        discount: productCard.querySelector('.discount')?.innerText,
        image: productCard.querySelector('img').src,
        category: productCard.querySelector('.category').innerText,
        name: productCard.querySelector('.name').innerText,
        price: productCard.querySelector('.discounted-price')?.innerText ||
               productCard.querySelector('.original-price')?.innerText ||
               productCard.querySelector('.original-prices')?.innerText,
        stock: productCard.getAttribute('data-stock')
    };

    const index = favorites.findIndex(item => item.id === productId);

    if (index > -1) {
        favorites.splice(index, 1);
        button.querySelector('i').classList.remove('active');
    } else {
        favorites.push(product);
        button.querySelector('i').classList.add('active');
    }

    favoriteCount.innerText = favorites.length;
    updateFavoriteList();
    saveFavorites();
}

function updateFavoriteList() {
    favoriteList.innerHTML = '';
    favorites.forEach(product => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><img src="${product.image}" alt="${product.name}" class="favorite-product-image"></td>
            <td>${product.name}</td>
            <td>${product.price}</td>
            <td>${product.stock}</td>
            <td>
                <button class="add-to-cart" onclick="addToCartFromFavorites('${product.id}')">Добавить в корзину</button>
                <button class="remove-from-favorites" onclick="removeFromFavorites('${product.id}')">Удалить</button>
            </td>
        `;
        favoriteList.appendChild(tr);
    });
}

function removeFromFavorites(productId) {
    favorites = favorites.filter(item => item.id !== productId);
    const productCard = document.querySelector(`.product-card[data-id="${productId}"] .add-to-favorites i`);
    if (productCard) {
        productCard.classList.remove('active');
    }
    favoriteCount.innerText = favorites.length;
    updateFavoriteList();
    saveFavorites();
}

function toggleModal(modal) {
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
}

favoriteButton.addEventListener('click', () => toggleModal(favoritesModal));
favoritesClose.addEventListener('click', () => toggleModal(favoritesModal));
cartButton.addEventListener('click', () => toggleModal(cartModal));
cartClose.addEventListener('click', () => toggleModal(cartModal));

window.addEventListener('click', function(event) {
    if (event.target === favoritesModal) {
        toggleModal(favoritesModal);
    }
    if (event.target === cartModal) {
        toggleModal(cartModal);
    }
});

function toggleCart(button) {
    const productCard = button.closest('.product-card');
    const productId = productCard.getAttribute('data-id');
    const product = {
        id: productId,
        image: productCard.querySelector('img').src,
        name: productCard.querySelector('.name').innerText,
        price: productCard.querySelector('.discounted-price')?.innerText ||
               productCard.querySelector('.original-price')?.innerText ||
               productCard.querySelector('.original-prices')?.innerText,
        quantity: 1
    };

    const index = cart.findIndex(item => item.id === productId);

    if (index > -1) {
        cart[index].quantity += 1;
    } else {
        cart.push(product);
    }

    cartCount.innerText = cart.length;
    updateCartList();
    saveCart();
}

function addToCartFromFavorites(productId) {
    const product = favorites.find(item => item.id === productId);
    toggleCart(document.querySelector(`.product-card[data-id="${productId}"] .add-to-cart`));
}

function updateCartList() {
    cartList.innerHTML = '';
    cart.forEach(product => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><img src="${product.image}" alt="${product.name}" class="cart-product-image"></td>
            <td>${product.name}</td>
            <td class="cart-item-price">${product.price}</td>
            <td>
                <button class="quantity-change" onclick="changeQuantity('${product.id}', -1)">-</button>
                <span class="cart-item-quantity">${product.quantity}</span>
                <button class="quantity-change" onclick="changeQuantity('${product.id}', 1)">+</button>
            </td>
            <td>
                <button class="remove-from-cart" onclick="removeFromCart('${product.id}')">Удалить</button>
            </td>
        `;
        cartList.appendChild(tr);
    });
}

function changeQuantity(productId, delta) {
    const index = cart.findIndex(item => item.id === productId);
    if (index > -1) {
        cart[index].quantity += delta;
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
    }
    updateCartList();
    saveCart();
    updateTotalPrice();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    cartCount.innerText = cart.length;
    updateCartList();
    saveCart();
    updateTotalPrice();
}

function updateTotalPrice() {
    let totalPrice = 0;
    cart.forEach(product => {
        const price = parseFloat(product.price.replace('$', ''));
        totalPrice += price * product.quantity;
    });
    document.getElementById('total-price').innerText = '$' + totalPrice.toFixed(2);
}

function buyItems() {
    alert('Оплата произведена, теперь у вас нет денег и нет товара 🤡');
    cart = [];
    cartCount.innerText = cart.length;
    updateCartList();
    saveCart();
    updateTotalPrice();
    toggleCartModal();
}

function toggleCartModal() {
    cartModal.style.display = cartModal.style.display === 'block' ? 'none' : 'block';
}

cartButton.addEventListener('click', toggleCartModal);
cartClose.addEventListener('click', toggleCartModal);

window.addEventListener('click', function(event) {
    if (event.target === cartModal) {
        toggleCartModal();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    favoriteCount.innerText = favorites.length;
    cartCount.innerText = cart.length;
    updateFavoriteList();
    updateCartList();
    updateTotalPrice();

    // Обновление состояния кнопок на карточках товаров при загрузке страницы
    document.querySelectorAll('.product-card').forEach(card => {
        const productId = card.getAttribute('data-id');
        if (favorites.find(item => item.id === productId)) {
            card.querySelector('.add-to-favorites i').classList.add('active');
        }
        if (cart.find(item => item.id === productId)) {
            // Примените нужные изменения, если необходимо для корзины
        }
    });
});






function setupScooterModal() {
    const scooterButton = document.getElementById('scooter-button');
    const scooterModal = document.getElementById('scooter-modal');
    const scooterModalClose = document.getElementById('scooter-modal-close');
    const addScooterButton = document.getElementById('add-scooter');
    const loginButton = document.getElementById('login-button');
  
    scooterButton.addEventListener('click', () => {
      scooterModal.style.display = 'block';
    });
  
    scooterModalClose.addEventListener('click', () => {
      scooterModal.style.display = 'none';
    });
  
    window.addEventListener('click', (event) => {
      if (event.target === scooterModal) {
        scooterModal.style.display = 'none';
      }
    });
  
    addScooterButton.addEventListener('click', () => {
      const type = document.getElementById('scooter-type').value;
      const manufacturer = document.getElementById('scooter-manufacturer').value;
      const model = document.getElementById('scooter-model').value;
      alert(`Добавлен скутер: Тип - ${type}, Производитель - ${manufacturer}, Модель - ${model}`);
      scooterModal.style.display = 'none';
    });
  
    loginButton.addEventListener('click', () => {
      // Перенаправление на страницу авторизации или открытие модального окна авторизации
      alert('Перенаправление на страницу авторизации');
    });
  }
  
  // Вызываем функцию setupScooterModal после загрузки контента страницы
  document.addEventListener('DOMContentLoaded', setupScooterModal);
  
  addScooterButton.addEventListener('click', () => {
    const type = document.getElementById('scooter-type').value;
    const manufacturer = document.getElementById('scooter-manufacturer').value;
    const model = document.getElementById('scooter-model').value;

    // Обновляем данные в блоке scooter-details
    document.getElementById('scooter-type-display').textContent = `Тип: ${type}`;
    document.getElementById('scooter-manufacturer-display').textContent = `Производитель: ${manufacturer}`;
    document.getElementById('scooter-model-display').textContent = `Модель: ${model}`;
    document.getElementById('scooter-image').src = `image/scooter_${type}_${manufacturer}_${model}.png`;

    // Отображаем блок scooter-details
    document.getElementById('scooter-details').style.display = 'block';

    // Закрываем модальное окно
    scooterModal.style.display = 'none';
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
  

  //работа
  function showApplicationForm() {
    document.getElementById('applicationModal').style.display = 'block';
}

function closeApplicationForm() {
    document.getElementById('applicationModal').style.display = 'none';
}

document.getElementById('applicationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Ваша заявка отправлена!');
    closeApplicationForm();
});


function filterJobs() {
    const searchTerm = document.getElementById('search-bar').value.toLowerCase();
    const vacancies = document.querySelectorAll('.vacancy-card');
    
    vacancies.forEach(vacancy => {
        const title = vacancy.querySelector('h3').textContent.toLowerCase();
        const description = vacancy.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            vacancy.style.display = 'block';
        } else {
            vacancy.style.display = 'none';
        }
    });
}
