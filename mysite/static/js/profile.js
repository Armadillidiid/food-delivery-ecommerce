// Highlight selected nav based on route
const profileSidenav = document.querySelectorAll("#profile-sidenav div");
const route = document.querySelector("#profile-sidenav").dataset.route;
const profileSidenavLink = document.querySelectorAll("#profile-sidenav div a");
const pageBoard = document.querySelector("#page-board");
const pageBoardOpenHour = document.querySelector("#page-board-open-hour");
const pageBoardProduct = document.querySelector("#page-board-product");
const form = document.querySelectorAll("form");

for (const [i, option] of profileSidenav.entries()) {
  if (option.id == route) {
    option.classList.remove("bg-white");
    option.classList.add(
      "light-gray",
      "border-start",
      "border-4",
      "border-danger"
    );
    profileSidenavLink[i].href = "javascript:void(0)";
  }

  if (option.id == "open-hour") {
    profileSidenavLink[i].href = "javascript:void(0)";
    profileSidenav[i].addEventListener("click", () =>
      showPageOpenHour(i, option)
    );
  }

  if (option.id == "product") {
    profileSidenavLink[i].href = "javascript:void(0)";
    profileSidenav[i].addEventListener("click", () =>
      showPageProduct(i, option)
    );
  }

  if (option.id == "vendor") {
    profileSidenav[i].addEventListener("click", () => {
        showPageBoard(i, option);
    });
  }
}

function showPageBoard(i, option) {
  for (let j = 1; j < 3; j++) {
    profileSidenav[i + j].classList.add("bg-white");
    profileSidenav[i + j].classList.remove(
      "light-gray",
      "border-start",
      "border-4",
      "border-danger"
    );
  }

  option.classList.remove("bg-white");
  option.classList.add(
    "light-gray",
    "border-start",
    "border-4",
    "border-danger"
  );

  pageBoardOpenHour.classList.add("visually-hidden", "w-auto");
  pageBoardProduct.classList.add("visually-hidden", "w-auto");
  pageBoard.classList.remove("visually-hidden", "w-auto");
}

function showPageProduct(i, option) {
  for (let j = 2; j > 0; j--) {
    profileSidenav[i - j].classList.add("bg-white");
    profileSidenav[i - j].classList.remove(
      "light-gray",
      "border-start",
      "border-4",
      "border-danger"
    );
  }

  option.classList.remove("bg-white");
  option.classList.add(
    "light-gray",
    "border-start",
    "border-4",
    "border-danger"
  );

  pageBoard.classList.add("visually-hidden", "w-auto");
  pageBoardOpenHour.classList.add("visually-hidden", "w-auto");
  pageBoardProduct.classList.remove("visually-hidden", "w-auto");
}

function showPageOpenHour(i, option) {
  profileSidenav[i - 1].classList.add("bg-white");
  profileSidenav[i - 1].classList.remove(
    "light-gray",
    "border-start",
    "border-4",
    "border-danger"
  );
  profileSidenav[i + 1].classList.add("bg-white");
  profileSidenav[i + 1].classList.remove(
    "light-gray",
    "border-start",
    "border-4",
    "border-danger"
  );

  option.classList.remove("bg-white");
  option.classList.add(
    "light-gray",
    "border-start",
    "border-4",
    "border-danger"
  );

  pageBoard.classList.add("visually-hidden", "w-auto");
  pageBoardProduct.classList.add("visually-hidden", "w-auto");
  pageBoardOpenHour.classList.remove("visually-hidden", "w-auto");
}