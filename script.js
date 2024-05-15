//поиск

function search() {
    var searchTerm = document.getElementById("searchInput").value.toLowerCase();
    var itemsToSearch = document.querySelectorAll('.searchable');
    itemsToSearch.forEach(function(item) {
      if (item.textContent.toLowerCase().includes(searchTerm)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
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
