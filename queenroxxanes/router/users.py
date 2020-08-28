'''This is the Users router. It will handle HTTP requests for Users.'''

from flask import request, make_response, jsonify, Blueprint
from queenroxxanes.models.users import User, Client, Manager
from queenroxxanes.logging.logger import get_logger
from queenroxxanes.data.db import login, read_user_by_username, create_client, create_manager, \
                                 read_all_users, read_appointment_info_by_users_current_appointments, \
                                 update_user_info, read_user_by_id, delete_user

users = Blueprint('users', __name__)

_log = get_logger(__name__)


@users.route('/users', methods=['GET', 'POST', 'DELETE'])
def route_login():
    '''This is the route for login.'''
    if request.method == 'POST':
        # getting the user information from the form and getting the information from the db
        input_dict = request.get_json(force=True)
        user_username = input_dict['user']
        user_password = input_dict['password']
        user = login(user_username, user_password)
        if user:
            # Generate our token
            auth_token = user.encode_auth_token()
            _log.debug(dir(auth_token))
            response = make_response(jsonify(user.to_dict()))
            response.set_cookie('authorization', auth_token.decode())
            return response, 200
        else:
            return {}, 401
    elif request.method == 'GET':
        auth_token = request.cookies.get('authorization')
        if auth_token:
            _log.debug(auth_token)
            _log.debug(User.decode_auth_token(auth_token))
            return jsonify(read_user_by_username(User.decode_auth_token(auth_token))), 200
        else:
            return {}, 401
    elif request.method == 'DELETE':
        empty = make_response({})
        empty.set_cookie('authorization', '')
        return empty, 204
    else:
        return '', 501

@users.route('/register', methods=['GET', 'POST'])
def create_user():
    '''This is user route for registration.'''
    _log.debug('Creating Client')
    required_fields = ['first_name', 'last_name', 'username', 'password']
    if request.method == 'POST':
        input_dict = request.get_json(force=True)
        _log.debug('User POST request received with body %s', input_dict)
        if all(field in input_dict for field in required_fields):
            first_name = input_dict['first_name']
            last_name = input_dict['last_name']
            username = input_dict['username']
            password = input_dict['password']
            new_client = Client(first_name, last_name, username, password)
            if create_client(new_client):
                return jsonify(new_client.to_dict()), 201
            else:
                return request.json, 400
        else:
            return request.json, 400
    else:
        empty = make_response({})
        empty.set_cookie('authorization', '')
        return empty, 204


@users.route('/users/<int:user_id>', methods=['GET','PUT'])
def get_user(user_id):
    if request.method == 'GET':
        _log.debug('GET request for users by ID')
        user = read_user_by_id(user_id)
        if user:
            return jsonify(read_user_by_id(user_id)), 200
    elif request.method == 'PUT':
        input_dict = request.get_json(force=True)
        if update_user_info(input_dict['_id'], {'username': input_dict['username'], 'password': input_dict['password']}):
            return request.json, 204
        else:
            return request.json, 400
    else:
        pass

@users.route('/userslist', methods=['GET', 'DELETE'])
def route_users():
    '''This is the user route for retrieving and deleting from the user collection.'''
    if request.method == 'GET':
        return_users = read_all_users()
        return {'userList': return_users}, 200
    elif request.method == 'DELETE':
        del_dict = request.get_json(force=True)
        if '_id' in del_dict:
            result = delete_user(del_dict['_id'])
            if result not in [None, 'Cannot delete a manager.']:
                return request.json, 200
        return {}, 400
    else:
        return {}, 400

@users.route('/users/current_appointments', methods = ['GET'])
def route_current_appointments():
    _log.debug('Here is the /users/current_appointments')
    if request.method == 'GET':
        _log.info('GET request for appointment info of appointment history')
        input_dict = request.args
        _log.debug(input_dict['_id'])
        if '_id' in input_dict:
            result = read_appointment_info_by_users_current_appointments(input_dict['_id'])
            _log.debug(result)
            return jsonify(result), 200
        else:
            return {}, 404
    else:
        return {}, 400



@users.route('/manager', methods=['GET','POST'])
def create_new_manager():
    '''This is the route for creating a new managers.'''
    _log.debug('Creating manager')
    required_fields = ['username', 'password']
    if request.method == 'POST':
        input_dict = request.get_json(force=True)
        _log.debug('User POST request received with body %s', input_dict)
        if all(field in input_dict for field in required_fields):
            username = input_dict['username']
            password = input_dict['password']
            new_manager = Manager(username, password)
            if create_manager(new_manager):
                return jsonify(new_manager.to_dict()), 201
            else:
                return request.json, 400
        else:
            return request.json, 400
    else:
        empty = make_response({})
        empty.set_cookie('authorization', '')
        return empty, 204
