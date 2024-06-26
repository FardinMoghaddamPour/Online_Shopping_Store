// noinspection JSUnresolvedReference,DuplicatedCode

document.addEventListener('DOMContentLoaded', function () {
    const orderSummary = JSON.parse(localStorage.getItem('orderSummary'));

    if (!orderSummary) {
        alert('No order summary available.');
        window.location.href = '/cart/';
        return;
    }

    fetchUserAddresses();

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
                <span class="text-lg font-semibold">$${parseFloat(item.price).toFixed(2)}</span>
            </div>
        `;
        orderItemsContainer.appendChild(orderItem);
    });

    document.getElementById('total-price').textContent = `$${parseFloat(orderSummary.total_price).toFixed(2)}`;
    document.getElementById('final-price').textContent = `$${parseFloat(orderSummary.total_price).toFixed(2)}`;


});

function fetchUserAddresses() {

    fetch('/api/addresses/')
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Fetched addresses:', data);
            renderAddresses(data);
        })
        .catch(error => console.error('Error fetching addresses:', error));
}

function renderAddresses(addresses) {
    const addressContainer = document.getElementById('create-address-div');
    addressContainer.innerHTML = '';

    if (addresses.length === 0) {
        addressContainer.innerHTML = '<p>No addresses available. Please add an address.</p>';
        return;
    }

    addresses.forEach(address => {
        const addressElement = document.createElement('div');
        addressElement.classList.add('address-item', 'p-4', 'bg-white', 'rounded', 'shadow', 'mb-4');
        addressElement.innerHTML = `
            <div>
                <p>Address: ${address.country}, ${address.city}, ${address.address}</p>
                <p>Zipcode: ${address.zipcode}</p>
            </div>
            <div id="action-btns">
                <button class="activate-btn" data-id="${address.id}" style="color: ${address.is_active ? 'gray' : 'green'}; margin-left: 10px;">
                    ${address.is_active ? 'Deactivate' : 'Activate'}
                </button>
            </div>
        `;

        addressContainer.appendChild(addressElement);

        addressElement.querySelector('.activate-btn').addEventListener('click', function () {
            const addressId = this.getAttribute('data-id');
            const action = address.is_active ? 'deactivate' : 'activate';
            toggleAddressActivation(addressId, action);
        });
    });
}

function toggleAddressActivation(addressId, action) {
    const url = `/api/addresses/${addressId}/${action}_address/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(response => {
            if (response.ok) {
                fetchUserAddresses();
            } else {
                console.error('Error toggling address activation:', response.statusText);
            }
        })
        .catch(error => console.error('Error toggling address activation:', error));
}

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
