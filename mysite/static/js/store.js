// Store category sidenav
const sidenav = document.querySelectorAll(".sidenav");
try {
  sidenav[0].classList.add("sidenav-link-style");
  sidenav.forEach((el) => {
    el.addEventListener("click", () => {
      // Remove effect from previous element
      for (element of sidenav) {
        if (element.classList.contains("sidenav-link-style")) {
          element.classList.remove("sidenav-link-style");
          element.classList.add("remove-link-style");
        }
      }

      // Add effect to element clicked
      el.classList.add("sidenav-link-style");
      el.classList.remove("remove-link-style");
    });
  });
}
catch(err) {
  console.log(err)
}

const storeBanner = document.querySelector('#store-banner')
const availability = document.querySelector('#store-banner div')
if (availability == null) {
  storeBanner.classList.add('brightness-50')
}