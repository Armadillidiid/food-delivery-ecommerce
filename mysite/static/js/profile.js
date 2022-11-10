// Highlight selected nav based on route
const profileSidenav = document.querySelectorAll("#profile-sidenav div.row")
const route = document.querySelector("#profile-sidenav").dataset.route

for (option of profileSidenav) {
    if (option.id == route) {
        option.classList.remove("bg-white")
        option.classList.add('light-gray', 'border-start', 'border-4', 'border-danger')
    }
}