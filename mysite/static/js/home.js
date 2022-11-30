const vendors = document.querySelectorAll('.vendors')
const searchBar = document.querySelector('#searchBar input')

searchBar.addEventListener('input', function() {
    let query = this.value
    query = query.toLowerCase()

    for(let vendor of vendors) {
        vendor_name = vendor.dataset.vendor.toLowerCase()
        if (vendor_name.includes(query)) {
            vendor.classList.remove('visually-hidden')
        }
        else {
            vendor.classList.add('visually-hidden')
        }
    }
})
