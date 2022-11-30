import Cookies from "/static/node_modules/js-cookie/dist/js.cookie.mjs";
const csrftoken = Cookies.get("csrftoken");

// Query server
async function queryGoogleMap(url, string) {
  // Send request to server
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
    body: JSON.stringify({
      string: string,
    }),
  });

  // Read JSON response
  try {
    let data = await response.json();
    displayLocation(data["predictions"]);
  } catch (e) {
    console.log(e);
  }
}

// Get location query string
let searchBox = document.querySelector("#searchBox");
let string = "";
let url = searchBox.dataset.url;

searchBox.addEventListener("keyup", function () {
  string = this.value;
  console.log(string);
  queryGoogleMap(url, string);
});

// Filter array & display location autocomplete
function displayLocation(data) {
  let searchBoxResult = document.querySelector("#searchBoxResult");
  let locationEntriesEl = document.querySelectorAll("#searchBoxResult button");

  // Remove old location display
  if (locationEntriesEl) {
    for (let el of locationEntriesEl) {
      el.remove();
    }
  }

  let main_text = [5];
  let secondary_text = [5];
  // Add new location to row
  for (let i = 0; i < data.length; i++) {
    main_text[i] = data[i]["structured_formatting"]["main_text"];
    secondary_text[i] = data[i]["structured_formatting"]["secondary_text"];
    let searchBoxResultHTML = `<button type="button" class="w-100 px-2 my-0 py-0 border-0 bg-white light-gray-hover"><div class="row m-0 px-3 py-1 border-1 border-bottom"><span class="row fs-7 text-black">${main_text[i]}</span><span class="row fs-7 text-secondary">${secondary_text[i]}</span></div></button>`;

    // Append div
    searchBoxResult.innerHTML += searchBoxResultHTML;
  }
  // On click
  locationEntriesEl = document.querySelectorAll("#searchBoxResult button");
  locationEntriesEl.forEach(function (el, index) {
    el.addEventListener("click", function () {
      searchBox.value = `${main_text[index]}, ${secondary_text[index]}`;
      console.log("hey");
    });
  });

  // Hide and show based on focus status
  searchBox.addEventListener("focus", function () {
    for (let el of locationEntriesEl) {
      el.classList.remove("visually-hidden");
    }
  });
  searchBox.addEventListener("focusout", function () {
    setTimeout(function () {
      for (let el of locationEntriesEl) {
        el.classList.add("visually-hidden");
      }
    }, 200);
  });
}

// Insert map location into searchbox
let map_location = {};
map_location["address"] = searchBox.dataset.address;
map_location["state"] = searchBox.dataset.state;
map_location["country"] = searchBox.dataset.country;
if (map_location["state"] != undefined && map_location["state"] != "") {
  searchBox.value = `${map_location["address"]},${map_location["state"]},${map_location["country"]}`;
}
