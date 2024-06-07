const navLinks = document.querySelector('.nav-links')
function onToggleMenu(e){
    e.name = e.name === 'menu' ? 'close' : 'menu'
    navLinks.classList.toggle('top-[9%]')
}

document.addEventListener('DOMContentLoaded', function () {
    const cartIcon = document.getElementById('cart-icon');
    cartIcon.addEventListener('click', function (event) {
        if (!isUserAuthenticated) {
            event.preventDefault();
            window.location.href = '/sign-in/';
        }
    });
});