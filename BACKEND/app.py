import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models import db, Event, Guest, Vendor
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning
db.init_app(app)
CORS(app)

# Flag to ensure tables are created only once
tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True

@app.route('/')
def index():
    return "Welcome to EventPlanner360 API"

@app.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.json
        logging.debug("Received data: %s", data)

        if not data.get('name') or not data.get('date') or not data.get('location'):
            logging.error("Missing required fields: %s", data)
            return jsonify({'message': 'Missing required fields'}), 400

        new_event = Event(
            name=data['name'], 
            date=data['date'], 
            location=data['location'], 
            description=data.get('description', ''),
            budget=data.get('budget', 0.0)
        )
        db.session.add(new_event)
        db.session.commit()
        logging.info("Event created successfully")
        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        logging.exception("Failed to create event")
        return jsonify({'message': 'Failed to create event', 'error': str(e)}), 500

@app.route('/events/<int:event_id>/guests', methods=['POST'])
def add_guest(event_id):
    try:
        data = request.json
        logging.debug("Received data: %s", data)
        
        new_guest = Guest(
            name=data['name'], 
            email=data['email'], 
            rsvp=data.get('rsvp', False),
            event_id=event_id
        )
        db.session.add(new_guest)
        db.session.commit()
        logging.info("Guest added successfully")
        return jsonify({'message': 'Guest added successfully'}), 201
    except Exception as e:
        logging.exception("Failed to add guest")
        return jsonify({'message': 'Failed to add guest', 'error': str(e)}), 500

@app.route('/events/<int:event_id>/vendors', methods=['POST'])
def add_vendor(event_id):
    try:
        data = request.json
        logging.debug("Received data: %s", data)
        
        new_vendor = Vendor(
            name=data['name'], 
            service=data['service'], 
            contact=data['contact'],
            event_id=event_id
        )
        db.session.add(new_vendor)
        db.session.commit()
        
        logging.info("Vendor added successfully")
        return jsonify({'message': 'Vendor added successfully'}), 201
    except Exception as e:
        logging.exception("Failed to add vendor")
        return jsonify({'message': 'Failed to add vendor', 'error': str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = Event.query.all()
        logging.debug("Fetched events: %s", events)
        return jsonify([{
            'id': event.id, 
            'name': event.name, 
            'date': event.date, 
            'location': event.location, 
            'description': event.description, 
            'budget': event.budget
        } for event in events])
    except Exception as e:
        logging.exception("Failed to get events")
        return jsonify({'message': 'Failed to get events', 'error': str(e)}), 500

@app.route('/events/<int:event_id>/guests', methods=['GET'])
def get_guests(event_id):
    try:
        guests = Guest.query.filter_by(event_id=event_id).all()
        logging.debug("Fetched guests for event %d: %s", event_id, guests)
        return jsonify([{
            'id': guest.id, 
            'name': guest.name, 
            'email': guest.email, 
            'rsvp': guest.rsvp
        } for guest in guests])
    except Exception as e:
        logging.exception("Failed to get guests")
        return jsonify({'message': 'Failed to get guests', 'error': str(e)}), 500

@app.route('/events/<int:event_id>/vendors', methods=['GET'])
def get_vendors(event_id):
    try:
        vendors = Vendor.query.filter_by(event_id=event_id).all()
        logging.debug("Fetched vendors: %s", vendors)
        return jsonify([{
            'id': vendor.id, 
            'name': vendor.name, 
            'service': vendor.service, 
            'contact': vendor.contact
        } for vendor in vendors])
    except Exception as e:
        logging.exception("Failed to get vendors")
        return jsonify({'message': 'Failed to get vendors', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
