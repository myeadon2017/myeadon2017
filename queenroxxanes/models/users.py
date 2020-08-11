'''Defines the model for users'''
import json
import jwt
import datetime

from queenroxxanes.logging.logger import get_logger

_log = get_logger(__name__)
_secret_key = '10101567unique'

class User():
    '''A class that defines how users should behave'''
    def __init__(self, username='', password=''):
        self._id = -1
        self.username = username
        self.password = password

    def get_id(self):
        '''Gets users ID'''
        return self._id    
    def get_username(self):
        '''Gets users username'''
        return self.username
    def get_password(self):
        '''Gets users password'''
        return self.password

    def set_id(self, user_id):
        self._id = user_id  
    def set_username(self, user_name):
        self.username = user_name
    
    def login(self, username, password):
        '''Confirms users username and password are a match'''
        if(self.username == username) and (self.password == password):
            return True
        return False
    
    def to_dict(self):
        '''Creates an instance of a user from a dictionary input'''
        return self.__dict__

    def encode_auth_token(self):
        ''' Generate an authentication token for this user '''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': self.username
            }
            _log.debug("payload set")
            return jwt.encode(payload, _secret_key, algorithm='HS256')
        except Exception as e:
            _log.exception('Encode failed.')
            return e
    @staticmethod
    def decode_auth_token(auth_token):
        ''' Decode the auth token to receive the id of user '''
        try:
            payload = jwt.decode(auth_token, _secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired. please login again.'
        except jwt.InvalidTokenError:
            return 'Token invalid. Please login.'


class Client(User):
    '''A class that defines how Clients should behave'''
    def __init__(self, first_name='', last_name='', username='', password=''):
        super().__init__(username, password)
        self.first_name = first_name
        self.last_name = last_name
        self.appointments = []
        '''appointments = [{appointment_id, appointment_type, date, time, price}]'''
        self.history = []
        '''history = [{auction_id, amount, w/l status}]'''
        self.payments = []
        '''payments = [{auction_id, amount, w/l status}]'''
    def get_firstname(self):
        '''Gets the clients first name'''
        return self.first_name
    def get_lastname(self):
        '''Gets the clients last name'''
        return self.last_name  
    def get_history(self):
        '''Gets clients history'''
        return self.history
    def get_appointments(self):
        '''Gets clients appointments'''
        return self.appointments
    def get_payments(self):
        '''Gets clients payments'''
        return self.payments

    def set_firstname(self, first_name):
        '''Takes in a first name'''
        self.first_name = first_name
    def set_lastname(self, last_name):
        '''Takes in a last name'''
        self.last_name = last_name
    def create_history(self, appointment_id, appointment_type, purchase_date, appointment_date, price):
        '''Takes in an auction id and the amount and status of a bid and appends it to history.'''
        add_dict = {'appointment_id': appointment_id, 'appointment_type': appointment_type, 'purchase_date': purchase_date, 'appointment_date': appointment_date, 'price': price}
        self.history.append(add_dict)
    def create_appointments(self, auction_id):
        '''Takes in an'''
        add_dict = {'auction_id': auction_id}
        self.history.append(add_dict)
    def create_payments(self, auction_id):
        '''Takes in an'''
        add_dict = {'auction_id': auction_id}
        self.history.append(add_dict)

    @classmethod
    def from_dict(cls, input_client):
        '''Creates an instance of a bidder from a dictionary input'''
        client = Client()
        client.__dict__.update(input_client)
        return client


class Manager(User):
    '''A class that defines how Managers should behave'''
    def __init__(self, username='', password=''):
        super().__init__(username, password)
        
    @classmethod
    def from_dict(cls, input_manager):
        '''Creates an instance of a Manager from a dictionary input'''
        manager = Manager()
        manager.__dict__.update(input_manager)
        return manager


class UserEncoder(json.JSONEncoder):
    ''' Allows us to serialize our objects as JSON '''
    def default(self, o):
        return o.to_dict()


