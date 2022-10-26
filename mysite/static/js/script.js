  function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", function () {
  // Auto hide nav-bar
  const autoHide = document.querySelector(".autohide");

  if (autoHide) {
    let lastScrollY = window.scrollY;
    let height = screen.height;    

    window.addEventListener("scroll", function () {
      if (lastScrollY < window.scrollY && lastScrollY > height) {
        autoHide.classList.remove("scrolled-up");
        autoHide.classList.add("scrolled-down");
        console.log("Scrolling down");
      } else {
        autoHide.classList.remove("scrolled-down");
        autoHide.classList.add("scrolled-up");
        console.log("Scrolling up");
      }

      lastScrollY = window.scrollY;
    });
  }

  // FAQ search bar
  const searchInput = document.getElementById("searchBar");
  const faqFromDOM = document.getElementsByClassName("accordion-button");

  searchInput.addEventListener("input", (e) => {
    const value = e.target.value;
    const searchQuery = value.toLowerCase();

    for (const nameElement of faqFromDOM) {
      let name = nameElement.textContent.toLowerCase();

      if (name.includes(searchQuery)) {
        nameElement.style.display = "block";
      } else {
        nameElement.style.display = "none";
      }
    }
  });
});


// Sidenav
const sidenav = document.querySelectorAll(".sidenav");
sidenav[0].classList.add('sidenav-link-style')
sidenav.forEach(el => {
  el.addEventListener('click', () => {
    // Remove effect from previous element
    for (element of sidenav){
      if (element.classList.contains("sidenav-link-style")){
        element.classList.remove("sidenav-link-style");
        element.classList.add("remove-link-style");
      }
    }

    // Add effect to element clicked
    el.classList.add("sidenav-link-style");
    el.classList.remove("remove-link-style")
  })
})

// Add to cart button
const addToCartBtn = document.getElementsByClassName("add-to-cart")

for (btn of addToCartBtn){
  btn.addEventListener('click', function() {
    let productId = this.dataset.product
    let action = this.dataset.action
    console.log('ProductId:', productId, 'Action:', action)
    updateUserCart()
  })
}