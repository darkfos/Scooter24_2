//поиск
var lastResFind = ""; // последний удачный результат
var copy_page = ""; // копия страницы в ихсодном виде

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

    if (document.body.innerHTML.indexOf(textToFind) == "-1")
        alert("Ничего не найдено, проверьте правильность ввода!");

    if (copy_page.length > 0)
        document.body.innerHTML = copy_page;
    else copy_page = document.body.innerHTML;


    document.body.innerHTML = document.body.innerHTML.replace(eval("/name=" + lastResFind + "/gi"), " "); //стираем предыдущие якори для скрола
    document.body.innerHTML = document.body.innerHTML.replace(eval("/" + textToFind + "/gi"), "<a class='highlighted' name=" + textToFind + ">" + textToFind + "</a>"); //Заменяем найденный текст ссылками с якорем;
    lastResFind = textToFind; // сохраняем фразу для поиска, чтобы в дальнейшем по ней стереть все ссылки
    window.location = '#' + textToFind; //перемещаем скрол к последнему найденному совпадению
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

//карусель
 $(document).ready(function(){
    $('.carousel').slick({
      infinite: true,
      slidesToShow: 4, // Количество отображаемых слайдов
      slidesToScroll: 2, // Количество прокручиваемых слайдов
    });
  });


  
//кнопка View more
let isHidden = true; 

function hideCards() {
  const productCards = document.querySelectorAll('.product-card');
  for (let i = 16; i < productCards.length; i++) {
    if (isHidden) {
      productCards[i].classList.add('hidden');
    } else {
      productCards[i].classList.remove('hidden');
    }
  }
}

function toggleVisibility() {
  isHidden = !isHidden; // Изменяем состояние флага
  hideCards(); // функция скрытия/отображения карточек
}

// Вызываем функцию hideCards() при загрузке страницы, чтобы скрыть лишние карточки
hideCards();

//кнопка "View more"
const viewMoreButton = document.querySelector('.view-more');

// обрабовпитчик клика на кнопку "View more"
viewMoreButton.addEventListener('click', toggleVisibility);


//баннер
// Отображение модального окна
function showModal() {
  const modal = document.getElementById('myModal');
  modal.style.display = 'block';
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
  const modal = document.getElementById('myModal');
  if (event.target == modal) {
    modal.style.display = 'none';
  }
}

// Переадресация на WhatsApp
function redirectToWhatsApp() {
  window.location.href = 'https://wa.me/номер_WhatsApp';
}
function redirectToTelegram() {
  window.location.href = 'https://t.me/Calm_the_loony';
}

// Инициирование звонка
function makePhoneCall() {
  window.location.href = 'tel:+9614277510';
}


//шапка сворачивается при отпределенном количестве прокрутки, позже доделать
let prevScrollPos = window.pageYOffset;
let isMenuOpen = false; // Флаг для отслеживания состояния меню

function scrollHandler(event) {
    const currentScrollPos = window.pageYOffset;
    const header = document.getElementById("header");
    const actionContainer = document.querySelector(".action-container");
    const submenu = document.querySelector('.submenu');

    if (prevScrollPos > currentScrollPos || currentScrollPos < actionContainer.offsetTop + actionContainer.offsetHeight) {
        header.style.height = "100px"; /* Показываем шапку при прокрутке вверх или если мы выше action-container */
        actionContainer.style.marginLeft = "0"; // Вернуть обычный margin-left
    } else {
        header.style.height = "50px"; /* Скрываем верхнюю часть шапки при прокрутке вниз и нахождении ниже action-container */
        submenu.style.display = 'none'; // Скрываем подменю при прокрутке вниз
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
    if (!isMenuOpen) {
        header.style.height = '100px'; // Вернуть обычную высоту
        logoText.style.opacity = '1'; 
        submenu.style.display = 'block'; // Показ подменю
        isMenuOpen = true;
    } else {
        // Иначе, свернуть шапку и скрыть подменю
        header.style.height = '50px';
        submenu.style.display = 'none';
        isMenuOpen = false;
    }
}


//открытие карточки товара


//избранное
// let favorites = [];
// const favoriteButton = document.getElementById('favorite-button');
// const favoriteCount = document.getElementById('favorite-count');
// const favoriteList = document.querySelector('#favorite-list tbody');
// const favoritesModal = document.getElementById('favorites-modal');
// const favoritesClose = document.getElementById('favorites-close');

// function toggleFavorite(button) {
//     const productCard = button.closest('.product-card');
//     const productId = productCard.getAttribute('data-id');
//     const product = {
//         id: productId,
//         discount: productCard.querySelector('.discount')?.innerText,
//         image: productCard.querySelector('img').src,
//         category: productCard.querySelector('.category').innerText,
//         name: productCard.querySelector('.name').innerText,
//         price: productCard.querySelector('.discounted-price')?.innerText ||
//                productCard.querySelector('.original-price')?.innerText ||
//                productCard.querySelector('.original-prices')?.innerText,
//         stock: productCard.getAttribute('data-stock')
//     };

//     const index = favorites.findIndex(item => item.id === productId);

//     if (index > -1) {
//         favorites.splice(index, 1);
//         button.querySelector('i').classList.remove('active');
//     } else {
//         favorites.push(product);
//         button.querySelector('i').classList.add('active');
//     }

//     favoriteCount.innerText = favorites.length;
//     updateFavoriteList();
// }

// function updateFavoriteList() {
//     favoriteList.innerHTML = '';
//     favorites.forEach(product => {
//         const tr = document.createElement('tr');
//         tr.innerHTML = `
//             <td><img src="${product.image}" alt="${product.name}" class="favorite-product-image"></td>
//             <td>${product.name}</td>
//             <td>${product.price}</td>
//             <td>${product.stock}</td>
//             <td>
//                 <button class="add-to-cart">Добавить в корзину</button>
//                 <button class="remove-from-favorites" onclick="removeFromFavorites('${product.id}')">Удалить</button>
//             </td>
//         `;
//         favoriteList.appendChild(tr);
//     });
// }

// function removeFromFavorites(productId) {
//     favorites = favorites.filter(item => item.id !== productId);
//     document.querySelector(`.product-card[data-id="${productId}"] .add-to-favorites i`).classList.remove('active');
//     favoriteCount.innerText = favorites.length;
//     updateFavoriteList();
// }

// function toggleModal() {
//     favoritesModal.style.display = favoritesModal.style.display === 'block' ? 'none' : 'block';
// }

// favoriteButton.addEventListener('click', toggleModal);
// favoritesClose.addEventListener('click', toggleModal);

// window.addEventListener('click', function(event) {
//     if (event.target === favoritesModal) {
//         toggleModal();
//     }
// });


//корзина
// document.addEventListener('DOMContentLoaded', (event) => {
//   let cart = [];
//   const cartButton = document.getElementById('cart-button');
//   const cartCount = document.getElementById('cart-count');
//   const cartList = document.querySelector('#cart-list tbody');
//   const cartModal = document.getElementById('cart-modal');
//   const cartClose = document.querySelector('.close');

//   function toggleCart(button) {
//       const productCard = button.closest('.product-card');
//       const productId = productCard.getAttribute('data-id');
//       const product = {
//           id: productId,
//           discount: productCard.querySelector('.discount')?.innerText,
//           image: productCard.querySelector('img').src,
//           category: productCard.querySelector('.category').innerText,
//           name: productCard.querySelector('.name').innerText,
//           price: productCard.querySelector('.discounted-price')?.innerText ||
//                  productCard.querySelector('.original-price')?.innerText,
//           quantity: 1
//       };

//       const index = cart.findIndex(item => item.id === productId);

//       if (index > -1) {
//           cart[index].quantity += 1;
//       } else {
//           cart.push(product);
//       }

//       cartCount.innerText = cart.length;
//       updateCartList();
//   }

//   function updateCartList() {
//       cartList.innerHTML = '';
//       cart.forEach(product => {
//           const tr = document.createElement('tr');
//           tr.innerHTML = `
//               <td><img src="${product.image}" alt="${product.name}" class="cart-product-image"></td>
//               <td>${product.name}</td>
//               <td>${product.price}</td>
//               <td>${product.quantity}</td>
//               <td>
//                   <button class="remove-from-cart" onclick="removeFromCart('${product.id}')">Удалить</button>
//               </td>
//           `;
//           cartList.appendChild(tr);
//       });
//   }

//   function removeFromCart(productId) {
//       const index = cart.findIndex(item => item.id === productId);
//       if (index > -1) {
//           cart.splice(index, 1);
//           cartCount.innerText = cart.length;
//           updateCartList();
//       }
//   }

//   function toggleCartModal() {
//       cartModal.style.display = cartModal.style.display === 'block' ? 'none' : 'block';
//   }

//   if (cartButton) {
//       cartButton.addEventListener('click', toggleCartModal);
//   }

//   if (cartClose) {
//       cartClose.addEventListener('click', toggleCartModal);
//   }

//   window.addEventListener('click', function(event) {
//       if (event.target === cartModal) {
//           toggleCartModal();
//       }
//   });

//   window.toggleCart = toggleCart;
// });

//избранное и корзина
let favorites = [];
let cart = [];

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
    document.querySelector(`.product-card[data-id="${productId}"] .add-to-favorites i`).classList.remove('active');
    favoriteCount.innerText = favorites.length;
    updateFavoriteList();
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
    updateTotalPrice();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    cartCount.innerText = cart.length;
    updateCartList();
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

//оплата
if (!cart) {
  let cart = [];
}
if (!cartButton) {
  const cartButton = document.getElementById('cart-button');
}
if (!cartCount) {
  const cartCountn = document.getElementById('cart-count');
}
if (!cartList) {
  const cartList = document.getElementById('#cart-list tbody');
}if (!cartModal) {
  const cartModal = document.getElementById('cart-modal');
}if (!cartClose) {
  const cartClose = document.getElementById('cart-close');
}


function toggleCart(button) {
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
        stock: productCard.getAttribute('data-stock'),
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
    updateTotalPrice();
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
    updateTotalPrice();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    cartCount.innerText = cart.length;
    updateCartList();
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


//выбор модели и перенаправление на авторизацию
// function setupScooterModal() {
//     const scooterButton = document.getElementById('scooter-button');
//     const scooterModal = document.getElementById('scooter-modal');
//     const scooterModalClose = document.getElementById('scooter-modal-close');
//     const addScooterButton = document.getElementById('add-scooter');
//     const loginButton = document.getElementById('login-button');
  
//     scooterButton.addEventListener('click', () => {
//       scooterModal.style.display = 'block';
//     });
  
//     scooterModalClose.addEventListener('click', () => {
//       scooterModal.style.display = 'none';
//     });
  
//     window.addEventListener('click', (event) => {
//       if (event.target === scooterModal) {
//         scooterModal.style.display = 'none';
//       }
//     });
  
//     addScooterButton.addEventListener('click', () => {
//       const type = document.getElementById('scooter-type').value;
//       const manufacturer = document.getElementById('scooter-manufacturer').value;
//       const model = document.getElementById('scooter-model').value;
//       alert(`Добавлен скутер: Тип - ${type}, Производитель - ${manufacturer}, Модель - ${model}`);
//       scooterModal.style.display = 'none';
//     });
  
//     loginButton.addEventListener('click', () => {
//       // Перенаправление на страницу авторизации или открытие модального окна авторизации
//       alert('Перенаправление на страницу авторизации');
//     });
//   }
  
//   // Вызываем функцию setupScooterModal после загрузки контента страницы
//   document.addEventListener('DOMContentLoaded', setupScooterModal);
  