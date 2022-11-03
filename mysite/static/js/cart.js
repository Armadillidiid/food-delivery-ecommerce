// Get cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");


// Main fucntion
async function updateUserCart(productId, action, vendor, quantity) {  
  console.log("Processing request");

  let url = "/update-cart/";

  // Send request to server
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
    body: JSON.stringify({
      productId: productId,
      action: action,
      vendor: vendor,
      quantity: quantity
    }),
  });

  // Read JSON response
  try {
    let data = await response.json();
    console.log(data);
    location.reload()
  } catch (e) {
    console.log(e);
  }
}


// Add to cart button
const addToCartBtn = document.getElementsByClassName("add-to-cart");

for (btn of addToCartBtn) {
  btn.addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let vendor = this.dataset.vendor
    console.log("ProductId:", productId, "Action:", action, "Vendor:", vendor);
    updateUserCart(productId, action, vendor);
  });
}


// Offcanvas default select option according to quantity
const selectOption = document.getElementsByClassName("offcanvasCartQuantity");
for (option of selectOption) {
  let quantity = option.dataset.quantity ;
  option.getElementsByTagName('option')[quantity].selected = 'selected'

  // Submit form on change 
  option.addEventListener("change", function() {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let vendor = this.dataset.vendor;
    selectedQuantity =  this.options[this.selectedIndex].value;
    console.log(selectedQuantity)
    console.log("ProductId:", productId, "Action:", action, "Vendor:", vendor, "Quantity:", selectedQuantity);
    updateUserCart(productId, action, vendor, selectedQuantity);
  })
}
