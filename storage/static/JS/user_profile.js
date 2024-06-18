// noinspection JSUnresolvedReference,DuplicatedCode

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
                <div id="delete-btn">
                    <button class="delete-btn" data-id="${address.id}" style="color: red; margin-left: 10px;">X</button>
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
                        this.parentElement.parentElement.remove();
                    } else {
                        throw new Error('Failed to delete address');
                    }
                })
                .catch(error => {
                    console.error('Error deleting address:', error);
                });
            });
        });
    })
    .catch(error => {
        console.error('Error fetching addresses:', error);
        addressContainer.innerHTML = '<p>Error loading addresses.</p>';
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