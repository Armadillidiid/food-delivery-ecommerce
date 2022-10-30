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

  if (searchInput) {
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
  }
});

// Sidenav
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

// Submit checkout form
const checkoutSubmit = document.querySelector("#checkoutSubmit")
const addNewAddress = document.querySelector("#addNewAddress")
try {
  checkoutSubmit.addEventListener("click", function() {
    console.log("Submitting form")
    addNewAddress.submit()
  })
}
catch(err) {
  console.log(err)
}

// Prepopulate edit checkout form
const addNewAddressInput = addNewAddress.getElementsByTagName('input')
const shippingAddressDisplay = document.querySelectorAll(".shippingAddressDisplay")
const shippingAddressEditBtn = document.querySelectorAll(".shippingAddressEditBtn")

shippingAddressEditBtn.forEach(function (btn, i) {
  btn.addEventListener("click", function() {
    addNewAddressInput[1].value = shippingAddressDisplay[i].dataset.contact_name
    addNewAddressInput[2].value = shippingAddressDisplay[i].dataset.address
    addNewAddressInput[3].value = shippingAddressDisplay[i].dataset.state
    addNewAddressInput[4].value = shippingAddressDisplay[i].dataset.city
    addNewAddressInput[5].value = shippingAddressDisplay[i].dataset.zip_code
    addNewAddressInput[6].value = shippingAddressDisplay[i].dataset.number.substring(4)
    addNewAddressInput[7].value = shippingAddressDisplay[i].dataset.id
  })
})

// for ( address of shippingAddressDisplay ){
//   for (let i = 0; i < addNewAddressInput.length; i++) {
//     if (i == 0) {
//       continue
//     }
//     console.log(addNewAddressInput[i])
//     // addNewAddressInput[i].value = address.dataset
//   }
// }

// Select first radio button in shipping address list
const addressButtonRadio = document.querySelectorAll("input[name='shippingAddresses']")
for ( radio of addressButtonRadio) {
  radio.checked = true;
  break
}

// Display addresss based on radio selected
addressButtonRadio.forEach(function (radio, i) {
  // Initialize non-first addresses hidden
  for ( let j = 0; j < shippingAddressDisplay.length; j++) {
    if (j != 0) {
      shippingAddressDisplay[j].classList.add("visually-hidden")
    } 
  }

  radio.addEventListener("change", function() {
    for (let j = 0; j < shippingAddressDisplay.length; j++) {
      if (j != i) {
        shippingAddressDisplay[j].classList.add("visually-hidden");
      }
      else {
        shippingAddressDisplay[j].classList.remove("visually-hidden");
      }
    }
  })
})

