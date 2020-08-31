import React, { Component } from 'react';
import { Card, Button, Form } from 'react-bootstrap';
import { connect } from 'react-redux';
import AppointmentService from '../services/appointment.service';
import UserService from '../services/user.service';
import { useHistory } from 'react-router-dom'


function FilterAppointments(props) {

    const appointmentService = props.appointmentService
    const getAppointmentList = props.getAppointmentList

    function appointmentDateValueChange(e) {
        if (e.target.value !== '' || e.target.value !== '0') {
            appointmentService.getAppointments({appointment_date: e.target.value}).then(res => {
                getAppointmentList(res.data.appointments)
            })
        }
        else {
            appointmentService.getAppointments().then(res => {
                getAppointmentList(res.data.appointments)
            })
        }
    }

    return (
        <>
            <Form>
                <Form.Group>
                    <Form.Label>Filter appointments by date...</Form.Label>
                    <input type="text" onChange={appointmentDateValueChange} />
                </Form.Group>
            </Form>
        </>
    )
}


function AppointmentCard(props) {
    const history = useHistory();

    let appointmentId = props.appointmentInfo._id
    let client_id = props.appointmentInfo.client_id
    let appointment_type = props.appointmentInfo.appointment_type
    let purchase_date = props.appointmentInfo.purchase_date
    let appointment_date = props.appointmentInfo.appointment_date
    let price = props.appointmentInfo.price

    function handleClick() {
        history.push(`/appointments/${appointmentId}`)
    }

    return(
        <div class="card-group w-30" style={{alignContent: 'center'}}>
            <Card style={{width: '18rem'}}>
                {/* <img src={prod_pic} class="card-img-top"></img> */}
                <Card.Title>
                    <div>
                        Client ID: {client_id}
                    </div>
                </Card.Title>
                <Card.Body>
                    <div>
                        <p>{appointment_type}</p>
                    </div>
                    <div>
                        Appointment Date: {appointment_date}
                    </div>
                    <div>
                        Purchase Date: {purchase_date}
                    </div>
                    <div>
                        Price: ${price}
                    </div>   
                </Card.Body>
                <Button onClick={handleClick}>Cancel Appointment</Button>
            </Card>
        </div>
    )
}

class AppointmentList extends Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        this.appointmentService.getAppointments().then(resp => {
            this.props.getAppointmentList(resp.data.appointments)
        })
    }

    appointmentService = new AppointmentService();

    fullAppointmentList(appointments) { 
        return (
            <>
                {
                    appointments.map((appointment) => {
                        return <AppointmentCard key={appointment._id} appointmentInfo={appointment} />
                    })
                }
            </>
        )
    }

    render() {
        console.log(this.props.appointmentList)
        if(this.props.appointmentList && this.props.appointmentList.length !== 0) {
            return (
                <>
                    <FilterAppointments appointmentService={this.appointmentService} getAppointmentList={this.props.getAppointmentList}></FilterAppointments>
                    { 
                        this.fullAppointmentList(this.props.appointmentList) 
                    }
                </>
                )
        }
        else {
            return(
                <>
                    <FilterAppointments appointmentService={this.appointmentService} getAppointmentList={this.props.getAppointmentList}></FilterAppointments>
                    <h1>No Appointments</h1>
                </>
            )
        }
    }
}

function mapStateToProps(state) {
    const { appointmentList } = state;
    return { appointmentList: appointmentList }
}

function mapDispatchToProps(dispatch) {
    return {
        getAppointmentList: (list) => dispatch({type: 'loadAppointmentList', appointmentList: list})
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(AppointmentList)