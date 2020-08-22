'''This is the appointments router. It will handle HTTP requests for Appointments.'''

import datetime
from flask import Blueprint, jsonify, request
from queenroxxanes.logging.logger import get_logger
from queenroxxanes.data.db import create_appointment, read_appointments_from_query, read_appointment_by_id
from queenroxxanes.models.appointments import Appointment
from queenroxxanes.models.users import Client
_log = get_logger(__name__)

appointments = Blueprint('appointments', __name__)

@appointments.route('/appointments', methods=['GET', 'POST'])
def appointments_main():
    '''This is the main /auctions route'''
    required_fields = ['client_id', 'appointment_type', 'appointment_date']
    if request.method == 'POST':
        input_dict = request.get_json(force=True)
        _log.debug('Appointment POST request received with body %s', input_dict)
        if all(field in input_dict for field in required_fields):
            client_id = input_dict['client_id']
            appointment_type = input_dict['appointment_type']
            appointment_date = input_dict['appointment_date']
            new_appointment = Appointment(client_id, appointment_type, appointment_date)
            create_appointment(new_appointment)
            return jsonify(new_appointment.to_dict()), 201
        else:
            return request.json, 400
    elif request.method == 'GET':
        # The GET request will either return all appointments or return them based on query info
        if len(request.args) == 0:
            return {'appointments': read_appointments_from_query({})}, 200
        elif query_dict = dict(request.args)
            for query in query_dict:
                try:
                    query_dict[query] = int(query_dict[query])
                    if query == 'client_id':
                        user_id = query_dict[query]
                        query_dict[query] = {'$eq': query_dict[query]}
                        _log.debug(query_dict[query])
                        _log.debug(user_id)
                except ValueError as err:
                    _log.error('Could not cast value to int, moving on...')
            _log.debug(query_dict)
            return_appointments = read_appointments_from_query(query_dict)
            return {'appointments': return_appointments}, 200
        else:
            query_dict = dict(request.args)
            for query in query_dict:
                try:
                    query_dict[query] = str(query_dict[query])
                    if query == 'appointment_date':
                        date = query_dict[query]
                        query_dict[query] = {'$eq': query_dict[query]}
                        _log.debug(query_dict[query])
                        _log.debug(date)
                except ValueError as err:
                    _log.error('Could not cast value to str, moving on...')
            _log.debug(query_dict)
            return_appointments = read_appointments_from_query(query_dict)
            return {'appointments': return_appointments}, 200
    else:
        return 'Not implemented', 501

@appointments.route('/appointments/<appointment_id>', methods=['GET'])
def appointments_with_id(appointment_id):
    '''This is for requests associated with an Appointment ID'''
    if request.method == 'GET':
        _log.debug('GET request for Auctions by ID')
        appointment = read_appointment_by_id(appointment_id)
        if appointment:
            return jsonify(read_appointment_by_id(appointment_id)), 200