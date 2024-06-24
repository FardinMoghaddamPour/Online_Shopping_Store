// noinspection JSUnresolvedReference,JSUnusedLocalSymbols

document.addEventListener('DOMContentLoaded', function () {
    fetchCartItems();

    function fetchCartItems() {
        fetch('/api/cart/')
            .then(response => response.json())
            .then(data => {
                renderCartItems(data.cart_items);
                updateTotalPrice(data.total_price);
                toggleCheckoutButton(data.cart_items.length > 0);
            })
            .catch(error => console.error('Error fetching cart items:', error));
    }

    function renderCartItems(cartItems) {
        const cartItemsContainer = document.getElementById('cart-items');
        cartItemsContainer.innerHTML = '';

        cartItems.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.dataset.productId = item.id;
            cartItem.innerHTML = `
                <div class="cart-item-details">
                    <h2 class="text-lg font-semibold">${item.name}</h2>
                    <p class="text-gray-700 cart-item-description">${item.description}</p>
                </div>
                <div class="cart-item-actions">
                    <span class="text-lg font-semibold">$${parseFloat(item.price).toFixed(2)}</span>
                    <div class="quantity-selector">
                        <button type="button" class="decrement" data-product-id="${item.id}">-</button>
                        <input type="number" id="quantity-${item.id}" name="quantity-${item.id}" value="${item.quantity}" readonly>
                        <button type="button" class="increment" data-product-id="${item.id}">+</button>
                    </div>
                    <button class="bg-red-500 text-white px-4 py-2 rounded-lg remove" data-product-id="${item.id}">Remove</button>
                </div>
            `;
            cartItemsContainer.appendChild(cartItem);

            cartItem.querySelector('.increment').addEventListener('click', () => updateQuantity(item.id, item.quantity + 1));
            cartItem.querySelector('.decrement').addEventListener('click', () => updateQuantity(item.id, item.quantity - 1));
            cartItem.querySelector('.remove').addEventListener('click', () => removeItem(item.id));
        });
    }

    function updateQuantity(productId, quantity) {
        if (quantity < 1) {
            removeItem(productId);
            return;
        }

        fetch('/api/update-cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ product_id: productId, quantity: quantity }),
        })
            .then(response => response.json())
            .then(data => {
                fetchCartItems();
            })
            .catch(error => console.error('Error updating cart:', error));
    }

    function removeItem(productId) {
        fetch('/api/remove-from-cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ product_id: productId }),
        })
            .then(response => response.json())
            .then(data => {
                fetchCartItems();
            })
            .catch(error => console.error('Error removing item from cart:', error));
    }

    function updateTotalPrice(totalPrice) {
        const totalPriceElement = document.getElementById('total-price');
        totalPriceElement.textContent = `$${parseFloat(totalPrice).toFixed(2)}`;
    }

    function toggleCheckoutButton(show) {
        const checkoutButton = document.getElementById('checkout-button');
        if (show) {
            checkoutButton.style.visibility = 'visible';
        } else {
            checkoutButton.style.visibility = 'hidden';
        }
    }

    document.getElementById('checkout-button').addEventListener('click', function () {
        fetch('/api/checkout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'Order created successfully') {
                    localStorage.setItem('orderSummary', JSON.stringify(data));
                    window.location.href = '/order-summary/';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error during checkout:', error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; cookies.length > i; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
