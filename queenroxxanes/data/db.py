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
appointments = db['appointments']
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
    if new_appointment.appointment_type == 'Eyebrow Appt':
        new_appointment.set_price(100)
        new_appointment.set_purchase_date(datetime.datetime.now())
    elif new_appointment.appointment_type == 'Hair Appt':
        new_appointment.set_price(200)
        new_appointment.set_purchase_date(datetime.datetime.now())
    elif new_appointment.appointment_type == 'Nail Appt':
        new_appointment.set_price(150)
        new_appointment.set_purchase_date(datetime.datetime.now())
    try:
        appointments.insert_one(new_appointment.to_dict())
        update_users_current_appointments(new_appointment.get_id(), new_appointment.get_client_id())
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

def read_appointment_info_by_users_current_appointments(user_id):
    '''Reads users current appointments'''
    client = Client.from_dict(read_user_by_id(int(user_id)))
    current_user_appointments = []
    for appointment in client.get_current_appointments():
        appt = read_appointment_by_id(int(appointment['_id']))
        _log.debug(appt)
        current_user_appointments.append({'appointment_id': appointment['_id'], 'appointment_type': appointment['appointment_type'], 'purchase_date': appointment['purchase_date'], 'appointment_date': appointment['appointment_date'], 'price': appointment['price']})
    return current_user_appointments

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
    
def update_users_current_appointments(appointment_id, client_id):
    '''Find and updates the current appointments list of the client involved'''
    appointment_id = int(appointment_id)
    client_id = int(client_id)
    query_string = {'_id': appointment_id}
    appt = Appointment.from_dict(read_appointment_by_id(appointment_id))
    if appt.get_client_id() == client_id:
        client_doc = read_user_by_id(client_id)
        try:
            client = Client.from_dict(client_doc)
            client.create_current_appointments(appointment_id, appt.get_appointment_type(), appt.get_purchase_date(), appt.get_appointment_date(), appt.get_price())
            users.update_one({'_id': client_id}, {'$set': client.to_dict()})
            op_success = client
            _log.info('Updated information for client ID %s', client_id)
        except TypeError as err:
            op_success = None
            _log.error('Encountered an error: %s', err)
        return op_success
    else:
        pass

def update_user_info(user_id: int, user_info: dict):
    '''Updates user information'''
    query_string = {'_id': int(user_id)}
    update_string = {'username': user_info['username'], 'password': user_info['password']}
    try:
        users.update_one(query_string, {'$set': update_string})
        op_success = user_info
        _log.info('Updated information for user ID %s', user_id)
    except:
        op_success = None
        _log.info('Could not update information for user ID %s', user_id)
    return op_success

def delete_user(user_id):
    '''Deletes a user with specified id. Rejects deletion if they are a manager.
    Also removes any active appointments with connected to user.'''
    user_query_string = {'_id': int(user_id)}
    try:
        user = read_user_by_id(user_id)
        if 'username' in user and user['username'] == 'manager':
            return 'Cannot delete a manager.'
        users.delete_one(user_query_string)
        op_success = user_id
        _log.info('Deleted user ID %s', user_id)
    except:
        op_success = None
        _log.info('Could not delete user ID %s', user_id)
    return op_success

# ID Counter Functions
def _get_user_id_counter():
    '''This function will get a unique ID by pulling it from the counter field of a counter
    document, then increase the counter value.'''
    return util.find_one_and_update({'_id': 'USERID_COUNTER'},
                                    {'$inc': {'count': 1}},
                                    return_document=pymongo.ReturnDocument.AFTER)['count']

def _get_appointment_id_counter():
    '''This function will get a unique ID by pulling it from the counter field of a counter
    document, then increase the counter value.'''
    return util.find_one_and_update({'_id': 'APPOINTMENTID_COUNTER'},
                                    {'$inc': {'count': 1}},
                                    return_document=pymongo.ReturnDocument.AFTER)['count']


if __name__ == "__main__":
    util.drop()
    users.drop()
    appointments.drop()

    util.insert_one({'_id': 'USERID_COUNTER', 'count': 0})
    util.insert_one({'_id': 'APPOINTMENTID_COUNTER', 'count': 0})

    users.create_index('username', unique=True)

    # Client
    client = Client('Matthew', 'Yeadon', 'username', 'password')
    create_client(client)
    # Manager
    manager = Manager('manager', 'password')
    create_manager(manager)

    # Appointment
    assigned_client = client
    appointment = Appointment(assigned_client.get_id(), 'Eyebrow Appt', '9/20/2020')
    create_appointment(appointment)
    

