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
    footer.classList.remove('bg-dark');
    footer.classList.add('bg-black');
}