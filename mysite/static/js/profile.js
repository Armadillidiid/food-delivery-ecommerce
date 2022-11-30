// Highlight selected nav based on route
const profileSidenav = document.querySelectorAll("#profile-sidenav div")
const route = document.querySelector("#profile-sidenav").dataset.route
const profileSidenavLink = document.querySelectorAll("#profile-sidenav div a")
const pageBoard = document.querySelector('#page-board')
const pageBoardOpenHour = document.querySelector('#page-board-open-hour')
const form = document.querySelectorAll('form')

for (const [i, option] of profileSidenav.entries()) {
    if (option.id == route) {
        option.classList.remove("bg-white")
        option.classList.add('light-gray', 'border-start', 'border-4', 'border-danger')
        profileSidenavLink[i].href = "javascript:void(0)";
    }

    if (option.id == 'open-hour') {
        profileSidenavLink[i].href = "javascript:void(0)";
        profileSidenav[i].addEventListener('click', function() {
            profileSidenav[i-1].classList.add("bg-white")
            profileSidenav[i-1].classList.remove('light-gray', 'border-start', 'border-4', 'border-danger')

            option.classList.remove("bg-white")
            option.classList.add('light-gray', 'border-start', 'border-4', 'border-danger')


            pageBoard.classList.add("visually-hidden", 'w-auto')
            pageBoardOpenHour.classList.remove('visually-hidden','w-auto')
        })
    }

    if (option.id == 'vendor') {
        profileSidenav[i].addEventListener('click', function() {
            profileSidenav[i+1].classList.add("bg-white")
            profileSidenav[i+1].classList.remove('light-gray', 'border-start', 'border-4', 'border-danger')

            option.classList.remove("bg-white")
            option.classList.add('light-gray', 'border-start', 'border-4', 'border-danger')


            pageBoardOpenHour.classList.add("visually-hidden", 'w-auto')
            pageBoard.classList.remove('visually-hidden', 'w-auto')
        })
    }
}
