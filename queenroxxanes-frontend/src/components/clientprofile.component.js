import React, { Component } from 'react';
import { Table } from 'react-bootstrap';
import { connect } from 'react-redux';
import AppointmentService from '../services/appointment.service';
import UserService from '../services/user.service';


function CurrentAppointmentTable(props) {
    let appointmentType = props.appointment.appointment_type
    let appointmentDate = props.appointment.appointment_date
    let appointmentPurchaseDate = props.appointment.purchase_date
    let appointmentPrice = props.appointment.price

    return(
        <tr>
            <td>{appointmentType}</td>
            <td>{appointmentDate}</td>
            <td>{appointmentPurchaseDate}</td>
            <td>${appointmentPrice}</td>
        </tr>
    )
}


class ClientProfile extends Component {
    
    userService = new UserService

    constructor(props) {
        super(props)
    }

    componentDidMount(){
        let appointmentIdArr = []
        for (let i = 0; i < this.props.user.current_appointments.length; i++){
            appointmentIdArr.push(this.props.user.current_appointments[i].appointment_id)
        }
        this.userService.getAppointmentInfoByUserID(this.props.user._id).then(resp =>
            {
                this.props.dispatch({type: 'loadCurrentAppointments', currentAppointments: resp.data})
            }
        )
    }


    fullappointmentList(user) {
        return (
            <Table striped bordered hover variant= "light">
                <thead>
                    <tr>
                        <th>Appointment Type</th>
                        <th>Appointment Date</th>
                        <th>Appointment Purchase Date</th>
                        <th>Appointment Price</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        user.current_appointments.map((appointment) => {
                            return <CurrentAppointmentTable prod={this.props.currentAppointments} appointment={appointment}/>
                        })
                    }
                </tbody>
            </Table>
        )
    }

    render() {
        console.log(this.props.user)
        if(this.props.user && this.props.user.current_appointments.length !== 0) {
            console.log('inside the if statement')
            return (this.fullappointmentList(this.props.user));
        }else{
            return(
                <>
                    <h1>You have no appointments yet.</h1>
                </>
            )
        }
    }
}

function mapStateToProps(state) {
    const { user, currentAppointments } = state;
    return { user: user, currentAppointments: currentAppointments }
}

export default connect(mapStateToProps)(ClientProfile);