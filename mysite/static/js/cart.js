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

// Update cart item quantity fucntion
async function updateUserCart(
  url,
  productId,
  action,
  vendor,
  quantity,
  orderId
) {
  console.log("Processing request");

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
      quantity: quantity,
      orderId: orderId,
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
    let url = "/update-cart/";
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let vendor = this.dataset.vendor;
    console.log("ProductId:", productId, "Action:", action, "Vendor:", vendor);
    updateUserCart(url, productId, action, vendor);
  });
}

// Offcanvas default select option according to quantity
const selectOption = document.getElementsByClassName("offcanvasCartQuantity");
for (option of selectOption) {
  quantity = option.dataset.quantity;
  option.getElementsByTagName("option")[quantity].selected = "selected";

  // Submit form on change
  option.addEventListener("change", function () {
    let url = "/update-cart/";
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let vendor = this.dataset.vendor;
    let orderId = null;
    selectedQuantity = this.options[this.selectedIndex].value;
    console.log(selectedQuantity);
    console.log(
      "ProductId:",
      productId,
      "Action:",
      action,
      "Vendor:",
      vendor,
      "Quantity:",
      selectedQuantity
    );
    updateUserCart(url, productId, action, vendor, selectedQuantity, orderId);
  });
}

// Delete cart
const deleteCartBtn = document.querySelector("#deleteCartBtn");
try {
  deleteCartBtn.addEventListener("click", function () {
    let url = "/delete-order/";
    let productId = null;
    let action = null;
    let vendor = this.dataset.vendor;
    let quantity = null;
    let orderId = this.dataset.orderid;
    updateUserCart(url, productId, action, vendor, quantity, orderId);
  });
} catch (err) {
  console.log("No cart exist to delete\n", err)
}
