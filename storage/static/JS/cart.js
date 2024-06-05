document.addEventListener('DOMContentLoaded', function () {
    fetchCartItems();

    function fetchCartItems() {
        fetch('/api/cart/')
            .then(response => response.json())
            .then(data => {
                renderCartItems(data.cart_items);
                updateTotalPrice(data.total_price);
            })
            .catch(error => console.error('Error fetching cart items:', error));
    }

    function renderCartItems(cartItems) {
        const cartItemsContainer = document.getElementById('cart-items');
        cartItemsContainer.innerHTML = '';

        cartItems.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
                <div class="cart-item-details">
                    <h2 class="text-lg font-semibold">${item.name}</h2>
                    <p class="text-gray-700 cart-item-description">${item.description}</p>
                </div>
                <div class="cart-item-actions">
                    <span class="text-lg font-semibold">$${item.price}</span>
                    <div class="quantity-selector">
                        <button type="button">-</button>
                        <input type="number" value="${item.quantity}" readonly>
                        <button type="button">+</button>
                    </div>
                    <button class="bg-red-500 text-white px-4 py-2 rounded-lg">Remove</button>
                </div>
            `;
            cartItemsContainer.appendChild(cartItem);
        });
    }

    function updateTotalPrice(totalPrice) {
        const totalPriceElement = document.getElementById('total-price');
        totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
    }
});