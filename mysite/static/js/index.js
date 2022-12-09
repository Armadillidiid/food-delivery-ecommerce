const navbar = document.querySelector('nav')
if (window.scrollY == 0) {
    navbar.classList.add('bg-transparent')
    navbar.classList.remove('bg-white')
}

window.addEventListener('scroll', function() {
    if (this.window.scrollY != 0) {
        navbar.classList.add('bg-white')
        navbar.classList.remove('bg-transparent')
    }
    else {
        navbar.classList.remove('bg-white')
        navbar.classList.add('bg-transparent')
    }
})

