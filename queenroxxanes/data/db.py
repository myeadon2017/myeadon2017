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

# Database and collection names