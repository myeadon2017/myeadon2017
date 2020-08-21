
from queenroxxanes.logging.logger import get_logger
_log = get_logger(__name__)

users = Blueprint('users', __name__)

'''This is the Users router. It will handle HTTP requests for Users.'''

from flask import request, make_response, jsonify, Blueprint
from queenroxxanes.models.users import User, Client, Manager
from queenroxxanes.logging.logger import get_logger
from queenroxxanes.data.db import login, read_user_by_username, create_client, create_manager, \
                                 read_all_users, read_appointment_info_by_users_current_appointments, \
                                 update_user_info