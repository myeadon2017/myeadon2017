''' This file will handle database functionality '''

import os
import datetime
import pymongo
from queenroxxanes.logging.logger import get_logger
from queenroxxanes.models.appointments import Appointment
from queenroxxanes.models.users import Client, Manager

_log = get_logger(__name__)

MONGO_URI = os.getenv('MONGO_URI')

# Initialize mongo conection
mongo = pymongo.MongoClient(MONGO_URI) # Open the database connection

# Database and collection 
db = mongo.queenroxxanes
util = db['utilities']
appointments = db['auctions']
users = db['users']

# Creation Operations
def create_client(new_client: Client):
    '''Create a Client in the database'''
    new_client.set_id(_get_user_id_counter())
    try:
        users.insert_one(new_client.to_dict())
        op_success = new_client
    except pymongo.errors.DuplicateKeyError as err:
        _log.error(err)
        op_success = None
    _log.info('Added %s ,Username: %s', new_client.get_firstname, new_client.get_username)
    return op_success

def create_manager(new_man: Manager):
    '''Create a Manager in the database'''
    new_man.set_id(_get_user_id_counter())
    try:
        users.insert_one(new_man.to_dict())
        op_success = new_man
    except pymongo.errors.DuplicateKeyError as err:
        _log.error(err)
        op_success = None
    _log.info('Added %s', new_man.get_username)
    return op_success

def create_appointment(new_appointment: Appointment):
    '''Create an Appointment in the database'''
    new_appointment.set_id(_get_appointment_id_counter())
    try:
        appointments.insert_one(new_appointment.to_dict())
        op_success = new_appointment
    except pymongo.errors.DuplicateKeyError as err:
        _log.error(err)
        op_success = None
    _log.info('Added appointment %s, %s', new_appointment.get_id(), new_appointment.get_appointment_type)
    return op_success


# Read operations
def read_all_users():
    '''Retrieve all users'''
    return list(users.find({}))

def read_all_clients():
    '''Retrieve all clients'''
    return users.find({'appointments': {'$exists': True}})

def read_user_by_id(user_id: int):
    '''Retrieve a User by their id in the database'''
    query_string = {'_id': int(user_id)}
    return users.find_one(query_string)

def read_user_by_username(username: str):
    '''Retrieve a user by their username'''
    query_string = {'username': username}
    return users.find_one(query_string)

def read_appointment_by_id(appointment_id: int):
    '''Retrieve a appointment by ID'''
    query_string = {"_id": appointment_id}
    return appointments.find_one(query_string)

def read_all_appointments():
    '''Retrieve all appointments'''
    return list(appointments.find({}))

def read_appointments_from_query(query_dict):
    '''Retrieves specified appointments based on query_dict'''
    returned_appointments = list(appointments.find(query_dict))
    return_struct = []
    for appointment in returned_appointments:
        appointment_doc = read_appointment_by_id(int(appointment['_id']))
        print(appointment)
        appointment['id'] = appointment_doc
        return_struct.append(appointment)
    return return_struct

def read_appointment_info_by_user_history(user_id):
    client = Client.from_dict(read_user_by_id(int(user_id)))
    appointment_history = []
    for appointment in client.get_history():
        appt = read_appointment_by_id(int(appointment['_id']))
        _log.debug(appt)
        appointment_history.append({'appointment_id': appointment['_id'], 'appointment_type': appointment['appointment_type'], 'purchase_date': appointment['purchase_date'], 'appointment_date': appointment['appointment_date'], 'price': appointment['price']})
    return appointment_history

def login(username: str, password: str):
    '''A function that takes in a username and returns a user object with that username'''
    _log.debug('Attempting to retrieve user from database')
    query_dict = {'username': username}
    user_dict = users.find_one(query_dict)
    if user_dict['password'] == password:
        _log.debug(user_dict)
        _log.debug(type(user_dict))
        # Ternary is "True value" if <condition> else "False Value"
        if user_dict:
            if 'first_name' in user_dict:
                return_user = Client.from_dict(user_dict)
            else:
                return_user = Manager.from_dict(user_dict)
        else:
            return_user = None
        return return_user
    else:
        return None

