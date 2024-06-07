// noinspection JSUnresolvedReference,UnnecessaryLocalVariableJS

document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            const productPrice = this.getAttribute('data-product-price');

            if (!isUserAuthenticated) {
                addToLocalStorageCart(productId, productName, productPrice);
            } else {
                addProductToCart(productId);
            }
        });
    });

    updateCartCountOnLoad();

    document.addEventListener('visibilitychange', function () {
        if (document.visibilityState === 'visible') {
            updateCartCountOnLoad();
        }
    });
});

function addToLocalStorageCart(productId, productName, productPrice) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    if (cart[productId]) {
        cart[productId].quantity += 1;
    } else {
        cart[productId] = {
            name: productName,
            price: productPrice,
            quantity: 1
        };
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateLocalStorageCartCount();
}

function updateLocalStorageCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const cartCount = Object.values(cart).reduce((acc, item) => acc + item.quantity, 0);
    // noinspection JSValidateTypes
    document.getElementById('cart-count').textContent = cartCount;
}

function addProductToCart(productId) {
    fetch('/api/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        updateCartCount();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateCartCount() {
    fetch('/api/get-cart-count/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const cartCountElement = document.getElementById('cart-count');
        cartCountElement.textContent = data.cart_count;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateCartCountOnLoad() {
    if (isUserAuthenticated) {
        updateCartCount();
    } else {
        updateLocalStorageCartCount();
    }
}

// noinspection DuplicatedCode
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
