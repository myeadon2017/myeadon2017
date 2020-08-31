import React, { Component } from 'react';
import { connect } from 'react-redux';
import AppointmentService from '../services/appointment.service';



class AppointmentForm extends Component {

    appointmentService = new AppointmentService();

    constructor(props){
        super(props);
        this.handleAppointmentTypeChange = this.handleAppointmentTypeChange.bind(this);
        this.handleAppointmentDateChange = this.handleAppointmentDateChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        let appointment = Object.assign({}, this.props.appointment);
        let user = Object.assign({}, this.props.user);

        appointment['client_id'] = this.props.user._id
        this.props.dispatch({type: 'handleAppointmentChange', appointment: appointment})
    }
    handleAppointmentTypeChange(e){
        let newAppointment = Object.assign({}, this.props.appointment);
        newAppointment.appointment_type = e.target.value;
        this.props.dispatch({type: 'handleAppointmentTypeChange', appointment: newAppointment})
        console.log('Appointment Type:', this.props.appointment)
    }
    handleAppointmentDateChange(e){
        let newAppointment = Object.assign({}, this.props.appointment);
        newAppointment.appointment_date = e.target.value;
        this.props.dispatch({type: 'handleAppointmentDateChange', appointment: newAppointment})
        console.log('Appointment Date:', this.props.appointment)
    }
    handleSubmit(e){
        e.preventDefault()
        this.appointmentService.createAppointment(this.props.appointment).then(
            (resp) => {
                this.props.dispatch({type: 'createAppointment', appointment: {'client_id': '', 'appointment_type': '', 'appointment_date': ''}})
                if (resp.status === 201){
                    alert("Successfully scheduled appointment.")
                } else {
                    alert("Could not schedule appointment.")
                }
            }
        )
    }

    render(){
        return(
            <div class="form-group w-25">
                <form onSubmit={this.handleSubmit}>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <h3 class="form-group">Schedule Appointment</h3>
                    </div>
                </div>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <h5 class="small_h5">Appointment Type:</h5>
                    </div>
                </div>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <input class="form-control" type="text" onChange={this.handleAppointmentTypeChange}/>
                        <div>For Appointment Type enter either: (Eyebrow Appt, Hair Appt or Nail Appt)</div>
                    </div>
                </div>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <h5 class="small_h5">Appointment Date:</h5>
                    </div>
                </div>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <input class="form-control" type="text" onChange={this.handleAppointmentDateChange}/>
                    </div>
                </div>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <button class="form-control" onClick={this.handleSubmit}>Submit</button>
                    </div>
                </div>    
                </form>
            </div>
        );
    }
}

function mapStateToProps(state){
    const { appointment, user } = state;
    return { appointment: appointment,
             user: user }
}

export default connect(mapStateToProps)(AppointmentForm);
