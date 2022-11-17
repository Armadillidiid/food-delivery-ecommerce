// Highlight selected nav based on route
const profileSidenav = document.querySelectorAll("#profile-sidenav div.row")
const route = document.querySelector("#profile-sidenav").dataset.route
const profileSidenavLink = document.querySelectorAll("#profile-sidenav div.row a")

for (const [i, option] of profileSidenav.entries()) {
    if (option.id == route) {
        option.classList.remove("bg-white")
        option.classList.add('light-gray', 'border-start', 'border-4', 'border-danger')
        profileSidenavLink[i].href = "javascript:void(0)";
    }
}