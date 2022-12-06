const vendors = document.querySelectorAll(".vendors");
const searchBar = document.querySelector("#searchBar input");
const forms = document.querySelectorAll('form')
const formSubmitBtn = document.querySelectorAll(".form-btn");


// Filter vendor by query text input
searchBar.addEventListener("input", function () {
  let query = this.value;
  query = query.toLowerCase();

  for (let vendor of vendors) {
    vendor_name = vendor.dataset.vendor.toLowerCase();
    if (vendor_name.includes(query)) {
      vendor.classList.remove("visually-hidden");
    } else {
      vendor.classList.add("visually-hidden");
    }
  }
});


// Add map_location along category filter form when submitted
formSubmitBtn[1].addEventListener('click', function() {
    let searchBoxInput = document.querySelector('#searchBox')
    let category = document.querySelector('#categoryFilter')
    category.appendChild(searchBoxInput)
})
