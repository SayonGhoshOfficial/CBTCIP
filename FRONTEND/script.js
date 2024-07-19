async function loadEvents() {
    try {
        const response = await fetch('http://127.0.0.1:5000/events');
        if (!response.ok) {
            throw new Error('Failed to fetch events');
        }
        const events = await response.json();
        const eventsList = document.getElementById('events-list');
        eventsList.innerHTML = '';

        events.forEach(event => {
            const eventItem = document.createElement('li');
            eventItem.classList.add('event-item');

            const eventDetails = document.createElement('div');
            eventDetails.classList.add('event-details');
            eventDetails.innerHTML = `
                <span class="event-name">${event.name}</span> - 
                <span class="event-date">${event.date}</span> - 
                <span class="event-location">${event.location}</span>
            `;
            eventItem.appendChild(eventDetails);

            const eventDescription = document.createElement('div');
            eventDescription.classList.add('event-description');
            eventDescription.textContent = event.description;
            eventItem.appendChild(eventDescription);

            const eventBudget = document.createElement('div');
            eventBudget.classList.add('event-budget');
            eventBudget.textContent = `Budget: ${event.budget}`;
            eventItem.appendChild(eventBudget);

            eventsList.appendChild(eventItem);
        });
    } catch (error) {
        console.error('Error loading events:', error.message);
    }
}

async function createEvent(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const eventData = {
        name: formData.get('event-name'),
        date: formData.get('event-date'),
        location: formData.get('event-location'),
        description: formData.get('event-description'),
        budget: parseFloat(formData.get('event-budget')) || 0.0
    };

    console.log('Sending data:', eventData); 

    try {
        const response = await fetch('http://127.0.0.1:5000/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(eventData)
        });
        if (!response.ok) {
            throw new Error('Failed to create event');
        }
        alert('Event created successfully');
        loadEvents();
    } catch (error) {
        console.error('Error creating event:', error.message);
        alert('Failed to create event');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadEvents();

    const eventForm = document.getElementById('event-form');
    eventForm.addEventListener('submit', createEvent);
});

document.getElementById('create-event-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let eventData = {
        name: document.getElementById('event-name').value,
        date: document.getElementById('event-date').value,
        location: document.getElementById('event-location').value,
        description: document.getElementById('event-description').value,
        budget: parseFloat(document.getElementById('event-budget').value)
    };

    fetch('http://127.0.0.1:5000/events', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(eventData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Event created successfully') {
            alert('Event created successfully');
        } else {
            alert('Failed to create event: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to create event');
    });
});
