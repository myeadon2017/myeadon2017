'''This module defines the module for appointments'''

class Appointment():
    '''Defines the attributes and behaviors of the Appointment class'''
    def __init__(self, appointment_type='', price=0):
        self._id = -1
        self.client_id = -1
        self.appointment_type = appointment_type
        self.purchase_date = None
        self.appointment_date = None
        self.price = price
    def get_id(self):
        '''return the id of the Appointment'''
        return self._id
    def get_client_id(self):
        '''returns the client id'''
        return self.client_id
    def get_appointment_type(self):
        '''returns the appointment type'''
        return self.appointment_type
    def get_purchase_date(self):
        '''returns the purchase date'''
        return self.purchase_date
    def get_appointment_date(self):
        '''returns the appointment date'''
        return self.appointment_date
    def get_price(self):
        '''returns the price'''
        return self.price
    
    def set_id(self, new_id):
        '''takes in a new ID'''
        self._id = new_id
    def set_client_id(self, client_id):
        '''takes in a new client ID'''
        self.client_id = client_id
    def set_appointment_type(self, appt_type):
        '''takes in a new appointment type'''
        self.appointment_type = appt_type
    def set_purchase_date(self, purchase_date):
        '''takes in a new purchase date'''
        self.purchase_date = purchase_date
    def set_appointment_date(self, appointment_date):
        '''takes in a new appointment date'''
        self.appointment_date = appointment_date
    def set_price(self, new_price):
        '''takes in a new price'''
        self.price = new_price