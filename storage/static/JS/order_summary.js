document.addEventListener('DOMContentLoaded', function () {
    const orderSummary = JSON.parse(localStorage.getItem('orderSummary'));

    if (!orderSummary) {
        alert('No order summary available.');
        window.location.href = '/cart/';
        return;
    }

    const orderItemsContainer = document.getElementById('order-items');
    orderSummary.order_items.forEach(item => {
        const orderItem = document.createElement('div');
        orderItem.classList.add('cart-item');
        orderItem.innerHTML = `
            <div class="cart-item-details">
                <h2 class="text-lg font-semibold">${item.name}</h2>
                <p class="text-gray-700">Quantity: ${item.quantity}</p>
            </div>
            <div class="cart-item-actions">
                <span class="text-lg font-semibold">$${item.price}</span>
            </div>
        `;
        orderItemsContainer.appendChild(orderItem);
    });

    document.getElementById('total-price').textContent = `$${orderSummary.total_price.toFixed(2)}`;
    document.getElementById('final-price').textContent = `$${orderSummary.total_price.toFixed(2)}`;
});
