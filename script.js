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
      slidesToScroll: 1, // Количество прокручиваемых слайдов
    });
  });

//кнопка View more
let isHidden = true; // Флаг для отслеживания состояния карточек

function hideCards() {
  const productCards = document.querySelectorAll('.product-card');
  // Проходимся по карточкам, начиная с 9-й (после второго ряда)
  for (let i = 16; i < productCards.length; i++) {
    // Добавляем или удаляем класс .hidden в зависимости от состояния флага
    if (isHidden) {
      productCards[i].classList.add('hidden');
    } else {
      productCards[i].classList.remove('hidden');
    }
  }
}

function toggleVisibility() {
  isHidden = !isHidden; // Изменяем состояние флага
  hideCards(); // Вызываем функцию скрытия/отображения карточек
}

// Вызываем функцию hideCards() при загрузке страницы, чтобы скрыть лишние карточки
hideCards();

// Получаем кнопку "View more"
const viewMoreButton = document.querySelector('.view-more');

// Назначаем обработчик клика на кнопку "View more"
viewMoreButton.addEventListener('click', toggleVisibility);




//шапка сворачивается при отпределенном количестве прокрутки 