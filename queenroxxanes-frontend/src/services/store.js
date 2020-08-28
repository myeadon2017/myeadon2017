import { createStore } from 'redux';

const initialState = {
    user: null, //username and password?
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    userList: [],
    currentAppointments: [],
    appointments: [],
    appointment: {'client_id': -1, 'appointment_type': '', 'appointment_date': ''},
    appointmentList: [],
    client: {},
    manager: {}
}


function queenRoxxaneReducer(state = initialState, action){
    switch(action.type){
        case 'login':
            return Object.assign({}, state, {username: '', user: action.user})
        case 'handleUsername':
            return Object.assign({}, state, {username: action.username})
        case 'handlePassword':
            return Object.assign({}, state, {password: action.password})
        case 'handleFirstName':
            return Object.assign({}, state, {firstName: action.firstName})
        case 'handleLastName':
            return Object.assign({}, state, {lastName: action.lastName})
        case 'handleAppointmentChange':
            return Object.assign({}, state, {appointment: action.appointment})
        case 'handleAppointmentTypeChange':
            return Object.assign({}, state, {appointment: action.appointment})
        case 'handleAppointmentDateChange':
            return Object.assign({}, state, {appointment: action.appointment})
        case 'createAppointment':
            return Object.assign({}, state, {appointment: action.appointment})
        case 'loadAppointmentList':
            return Object.assign({}, state, {appointmentList: action.appointmentList})
        case 'loadUserList':
            return Object.assign({}, state, {userList: action.userList})
        case 'loadAppointment':
            return Object.assign({}, state, {appointment: action.appointment})
        case 'loadUser':
            return Object.assign({}, state, {user: action.user})
        case 'removeUser':
            return Object.assign({}, state, {userList: action.userList})
        case 'handleUsernameChange':
            return Object.assign({}, state, {client: action.client})
        case 'handlePasswordChange':
            return Object.assign({}, state, {client: action.client})
        case 'handleFirstNameChange':
            return Object.assign({}, state, {client: action.client})
        case 'handleLastNameChange':
            return Object.assign({}, state, {client: action.client})
        case 'handleUserFieldChange':
            return Object.assign({}, state, {user: action.user})   
        case 'loadCurrentAppointments':
            return Object.assign({}, state, {currentAppointments: action.currentAppointments})
        case 'handleManUsernameChange':
            return Object.assign({}, state, {manager: action.manager})
        case 'handleManPasswordChange':
            return Object.assign({}, state, {manager: action.manager})
        default:
            return state;
    }
}




let store = createStore(queenRoxxaneReducer);

export default store;