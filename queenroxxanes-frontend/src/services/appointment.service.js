const { default: axios } = require('axios');

class AppointmentService{
    constructor(){
        this.URI = 'http://localhost:5000/appointments';
    }
    createAppointment(appointment){
        console.log('sending axios')
        return axios.post(this.URI, appointment, {withCredentials: true})
    }
    getAppointments(querydict) {
        console.log('sending axios get')
        return axios.get(this.URI, {withCredentials: true});
    }
}

export default AppointmentService;