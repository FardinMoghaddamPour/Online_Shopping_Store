// noinspection JSUnresolvedReference,DuplicatedCode,JSUnusedGlobalSymbols

document.addEventListener('DOMContentLoaded', function() {
    const addressContainer = document.querySelector('#addresses');

    fetch('/api/addresses/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        addressContainer.innerHTML = '';
        data.forEach(address => {
            const addressDiv = document.createElement('div');
            addressDiv.className = 'flex p-2 border-b border-gray-300';
            addressDiv.innerHTML = `
                <div>
                    <p>Address: ${address.country}, ${address.city}, ${address.address}</p>
                    <p>Zipcode: ${address.zipcode}</p>
                </div>
                <div id="action-btns">
                    <button class="delete-btn" data-id="${address.id}" style="color: red; margin-left: 10px;">X</button>
                    <button class="activate-btn" data-id="${address.id}" style="color: ${address.is_active ? 'gray' : 'green'}; margin-left: 10px;">
                        ${address.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                    <button class="edit-btn" onclick="window.location.href='/edit_address/${address.id}/'" style="color: blue; margin-left: 10px;">Edit</button>
                </div>
            `;
            addressContainer.appendChild(addressDiv);
        });

        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const addressId = this.getAttribute('data-id');
                fetch(`/api/addresses/${addressId}/delete_address/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        this.closest('.flex').remove();
                    } else {
                        throw new Error('Failed to delete address');
                    }
                })
                .catch(error => {
                    console.error('Error deleting address:', error);
                });
            });
        });

        const activateButtons = document.querySelectorAll('.activate-btn');
        activateButtons.forEach(button => {
            button.addEventListener('click', function() {
                const addressId = this.getAttribute('data-id');
                const isActive = this.textContent === 'Deactivate';
                const url = isActive
                    ? `/api/addresses/${addressId}/deactivate_address/`
                    : `/api/addresses/${addressId}/activate_address/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        if (isActive) {
                            this.textContent = 'Activate';
                            this.style.color = 'green';
                        } else {
                            document.querySelectorAll('.activate-btn').forEach(btn => {
                                btn.textContent = 'Activate';
                                btn.style.color = 'green';
                            });
                            this.textContent = 'Deactivate';
                            this.style.color = 'gray';
                        }
                    } else {
                        throw new Error(`Failed to ${isActive ? 'deactivate' : 'activate'} address`);
                    }
                })
                .catch(error => {
                    console.error(`Error ${isActive ? 'deactivating' : 'activating'} address:`, error);
                });
            });
        });
    })
    .catch(error => {
        console.error('Error fetching addresses:', error);
        addressContainer.innerHTML = '<p>Error loading addresses.</p>';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const ordersContainer = document.querySelector('#orders');

    fetch('/api/orders/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        ordersContainer.innerHTML = ''; // Clear any existing content
        data.forEach(order => {
            const orderDiv = document.createElement('div');
            orderDiv.className = 'border rounded-lg shadow-sm p-4 mb-4 bg-white';

            let orderItemsHtml = '<div class="mt-4">';
            order.order_items.forEach(item => {
                orderItemsHtml += `
                    <div class="border-b pb-2 mb-2">
                        <p class="font-semibold">Product Name: <span class="font-normal">${item.product_name}</span></p>
                        <p class="font-semibold">Quantity: <span class="font-normal">${item.quantity}</span></p>
                        <p class="font-semibold">Price: <span class="font-normal">$${item.price}</span></p>
                    </div>
                `;
            });
            orderItemsHtml += '</div>';

            orderDiv.innerHTML = `
                <div class="flex justify-between items-center mb-2">
                    <p class="font-semibold">Order Date: <span class="font-normal">${new Date(order.order_date).toLocaleDateString()}</span></p>
                    <p class="font-semibold">Total Price: <span class="font-normal">$${order.total_price}</span></p>
                    <p class="font-semibold">Status: <span class="font-normal">${order.status}</span></p>
                </div>
                ${orderItemsHtml}
            `;

            ordersContainer.appendChild(orderDiv);
        });
    })
    .catch(error => {
        console.error('Error fetching orders:', error);
        ordersContainer.innerHTML = '<p class="text-red-500">Error loading orders.</p>';
    });
});


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
