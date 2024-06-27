// noinspection DuplicatedCode,JSUnresolvedReference

document.addEventListener('DOMContentLoaded', function () {
    fetchOrderSummary();
    fetchUserAddresses();
    loadCouponFromLocalStorage();

    document.getElementById('check-coupon-button').addEventListener('click', function () {
        checkCoupon();
    });

    document.getElementById('create-address-button').addEventListener('click', function () {
        const form = document.getElementById('create-address-form');
        form.style.display = form.style.display === 'none' || form.style.display === '' ? 'block' : 'none';
    });

    document.getElementById('submit-address-button').addEventListener('click', function () {
        createAddress();
    });
});

function fetchOrderSummary() {
    fetch('/api/active-order/')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                window.location.href = '/cart/';
                return;
            }
            renderOrderSummary(data);
        })
        .catch(error => console.error('Error fetching order summary:', error));
}

function renderOrderSummary(data) {
    const orderItems = data.order_items;

    const orderItemsContainer = document.getElementById('order-items');
    orderItemsContainer.innerHTML = '';

    orderItems.forEach(item => {
        const orderItem = document.createElement('div');
        orderItem.classList.add('cart-item');
        // noinspection JSDeprecatedSymbols
        orderItem.innerHTML = `
            <div class="cart-item-details">
                <h2 class="text-lg font-semibold">${item.product.name}</h2>
                <p class="text-gray-700">Quantity: ${item.quantity}</p>
            </div>
            <div class="cart-item-actions">
                <span class="text-lg font-semibold">$${parseFloat(item.price).toFixed(2)}</span>
            </div>
        `;
        orderItemsContainer.appendChild(orderItem);
    });

    const totalPrice = parseFloat(data.total_price).toFixed(2);
    document.getElementById('total-price').textContent = `$${totalPrice}`;
    document.getElementById('final-price').textContent = `$${totalPrice}`;

    applyStoredDiscount();
}

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
        addressContainer.innerHTML = `
            <p class="text-red-500 font-bold">No addresses available. Please add an address.</p>
            <button id="create-address-button" class="bg-blue-500 text-white px-4 py-2 mb-1 rounded-lg">Create Address</button>
            <div id="create-address-form" class="grid grid-cols-1 gap-4 p-4 bg-white rounded-lg shadow-md" style="display: none;">
                <input type="text" id="country" placeholder="Country" class="border p-2 mb-1 rounded">
                <input type="text" id="city" placeholder="City" class="border p-2 rounded">
                <input type="text" id="address" placeholder="Address" class="border p-2 rounded">
                <input type="text" id="zipcode" placeholder="Zipcode" class="border p-2 rounded">
                <button id="submit-address-button" class="bg-green-500 text-white px-4 py-2 rounded-lg">Submit</button>
            </div>
        `;
        document.getElementById('create-address-button').addEventListener('click', function () {
            const form = document.getElementById('create-address-form');
            form.style.display = form.style.display === 'none' || form.style.display === '' ? 'block' : 'none';
        });

        document.getElementById('submit-address-button').addEventListener('click', function () {
            createAddress();
        });
        return;
    }

    const activeAddresses = addresses.filter(address => address.is_active);

    if (activeAddresses.length === 0) {
        addressContainer.innerHTML = '<p class="text-red-500 font-bold">No active addresses available. Please activate or create an address.</p>';
        addresses.forEach(address => {
            const addressElement = document.createElement('div');
            addressElement.classList.add('address-item', 'p-4', 'bg-white', 'rounded-lg', 'shadow-md', 'mb-4');
            addressElement.innerHTML = `
                <div>
                    <p>Address: ${address.country}, ${address.city}, ${address.address}</p>
                    <p>Zipcode: ${address.zipcode}</p>
                </div>
                <div id="action-btns">
                    <button class="activate-btn bg-green-500 text-white px-2 py-1 rounded" data-id="${address.id}" style="color: green; margin-left: 10px;">
                        Activate
                    </button>
                </div>
            `;
            addressContainer.appendChild(addressElement);
            addressElement.querySelector('.activate-btn').addEventListener('click', function () {
                const addressId = this.getAttribute('data-id');
                toggleAddressActivation(addressId, 'activate');
            });
        });
    } else {
        activeAddresses.forEach(address => {
            const addressElement = document.createElement('div');
            addressElement.classList.add('address-item', 'p-4', 'bg-white', 'rounded-lg', 'shadow-md', 'mb-4');
            addressElement.innerHTML = `
                <div>
                    <p>Address: ${address.country}, ${address.city}, ${address.address}</p>
                    <p>Zipcode: ${address.zipcode}</p>
                </div>
                <div id="action-btns">
                    <button class="activate-btn bg-gray-500 text-red-500 px-2 py-1 rounded" data-id="${address.id}" style="margin-left: 10px;">
                        Deactivate
                    </button>
                </div>
            `;
            addressContainer.appendChild(addressElement);
            addressElement.querySelector('.activate-btn').addEventListener('click', function () {
                const addressId = this.getAttribute('data-id');
                toggleAddressActivation(addressId, 'deactivate');
            });
        });
    }
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

function createAddress() {
    const country = document.getElementById('country').value;
    const city = document.getElementById('city').value;
    const address = document.getElementById('address').value;
    const zipcode = document.getElementById('zipcode').value;

    fetch('/api/create-address/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ country, city, address, zipcode }),
    })
        .then(response => {
            if (response.ok) {
                fetchUserAddresses();
                document.getElementById('create-address-form').style.display = 'none';
            } else {
                console.error('Error creating address:', response.statusText);
            }
        })
        .catch(error => console.error('Error creating address:', error));
}

function checkCoupon() {
    const couponCode = document.getElementById('coupon-code').value;

    fetch('/api/check-coupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ coupon: couponCode }),
    })
        .then(response => response.json())
        .then(data => {
            const couponInput = document.getElementById('coupon-code');
            const checkButton = document.getElementById('check-coupon-button');
            if (data.valid) {
                couponInput.classList.add('border-green-500');
                couponInput.classList.remove('border-red-500');
                couponInput.disabled = true;
                checkButton.style.display = 'none';
                // Save to local storage
                localStorage.setItem('coupon', JSON.stringify({ code: couponCode, discount: data.discount }));
                // Update the total price
                updateTotalPriceWithDiscount(data.discount);
            } else {
                couponInput.classList.add('border-red-500');
                couponInput.classList.remove('border-green-500');
            }
        })
        .catch(error => console.error('Error checking coupon:', error));
}

function updateTotalPriceWithDiscount(discount) {
    const finalPriceElement = document.getElementById('final-price');
    const currentFinalPrice = parseFloat(finalPriceElement.textContent.replace('$', ''));
    const newFinalPrice = currentFinalPrice - discount;
    finalPriceElement.textContent = `$${newFinalPrice.toFixed(2)}`;
}

function loadCouponFromLocalStorage() {
    const savedCoupon = localStorage.getItem('coupon');
    if (savedCoupon) {
        // noinspection JSUnusedLocalSymbols
        const { code, discount } = JSON.parse(savedCoupon);
        const couponInput = document.getElementById('coupon-code');
        const checkButton = document.getElementById('check-coupon-button');
        couponInput.value = code;
        couponInput.classList.add('border-green-500');
        couponInput.disabled = true;
        checkButton.style.display = 'none';
    }
}

function applyStoredDiscount() {
    const savedCoupon = localStorage.getItem('coupon');
    if (savedCoupon) {
        const { discount } = JSON.parse(savedCoupon);
        updateTotalPriceWithDiscount(discount);
    }
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
