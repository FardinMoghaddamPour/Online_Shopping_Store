// noinspection JSUnresolvedReference

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
            addressDiv.className = 'p-2 border-b border-gray-300';
            addressDiv.innerHTML = `
                <p>Address: ${address.country}, ${address.city}, ${address.address}</p>
                <p>Zipcode: ${address.zipcode}</p>
            `;
            addressContainer.appendChild(addressDiv);
        });
    })
    .catch(error => {
        console.error('Error fetching addresses:', error);
        addressContainer.innerHTML = '<p>Error loading addresses.</p>';
    });
});