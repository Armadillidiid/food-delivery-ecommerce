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
      } else {
        autoHide.classList.remove("scrolled-down");
        autoHide.classList.add("scrolled-up");
      }

      lastScrollY = window.scrollY;
    });
  }

  // FAQ search bar
  const searchInput = document.getElementById("searchBar");
  const faqFromDOM = document.getElementsByClassName("accordion-item");

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const value = e.target.value;
      const searchQuery = value.toLowerCase();

      for (const nameElement of faqFromDOM) {
        let name = nameElement.textContent.toLowerCase();

        if (name.includes(searchQuery)) {
          nameElement.classList.remove("visually-hidden")
        } else {
          nameElement.classList.add("visually-hidden")
        }
      }
    });
  }
});


// Change footer black
function changeFooterBackground() {
  const footer = document.querySelector("footer div");
    footer.classList.remove('dark-footer-bg');
    footer.classList.add('bg-black');
}


// Hide user select menu form
function hideUserForeignkey() {
  const userLabel = document.querySelector('#div_id_user')
  userLabel.classList.add('visually-hidden')
}

// Auto-hide searchbar thingis
const cartLogoutBtn = document.querySelector('#cart-logout-btn')
const navBrand = document.querySelector('#nav-brand')
const searchBarInput = document.querySelector('#searchBar')
if (cartLogoutBtn && navBrand) {
  let lastScrollY = window.scrollY;
  let height = 110;

  window.addEventListener("scroll", function () {
    let width = window.innerWidth
    if (lastScrollY < window.scrollY && lastScrollY > height && width < 576) {
      cartLogoutBtn.classList.add("visually-hidden");
      navBrand.classList.add("visually-hidden");
      searchBarInput.classList.remove("mt-2");
    } else {
      cartLogoutBtn.classList.remove("visually-hidden");
      navBrand.classList.remove("visually-hidden");
      searchBarInput.classList.add('mt-2')
    }

    lastScrollY = window.scrollY;
  });
}