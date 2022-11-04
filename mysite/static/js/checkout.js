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

// Continue paymnet
const continuePaymentBtn = document.querySelector("#continuePayment");
const paypalBtn = document.querySelector("#paypal-button-container")
continuePaymentBtn.addEventListener("click", function() {
  for (radio of addressButtonRadio) {
    if (radio.checked == true) {
      paypalBtn.classList.remove("visually-hidden");
      continuePaymentBtn.classList.add("visually-hidden");
      break;
    }
  }
})
