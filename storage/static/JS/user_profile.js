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
                </div>
            `;
            addressContainer.appendChild(addressDiv);
        });

        // Add event listeners for delete buttons
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const addressId = this.getAttribute('data-id');
                fetch(`/api/addresses/${addressId}/delete_address/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // Function to get CSRF token
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

        // Add event listeners for activate/deactivate buttons
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
                        'X-CSRFToken': getCookie('csrftoken')  // Function to get CSRF token
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

// Function to get CSRF token
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