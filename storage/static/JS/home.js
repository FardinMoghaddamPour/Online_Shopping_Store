document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');

            if (!isUserAuthenticated) {
                window.location.href = '/sign-in/';
            } else {
                addProductToCart(productId);
            }
        });
    });
});

function addProductToCart(productId) {
    console.log('Add product to cart:', productId);
}
