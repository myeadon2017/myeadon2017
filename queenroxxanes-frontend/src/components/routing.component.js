import React, { Component } from 'react';
import { Route, BrowserRouter as Router, Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import { connect } from 'react-redux';

import AppointmentList from './appointmentlist.component';
import ClientProfile from './clientprofile.component';
import AppointmentForm from './appointmentform.component';
import RegisterForm from './register.component';
import Login from './login.component';
import '../sass/nav.scss';


function UserNav(props) {
    const UserLoggedIn = props.user
    if (UserLoggedIn && 'username' in UserLoggedIn) {
        let username = UserLoggedIn.username
        console.log('has a username')
        console.log(UserLoggedIn.username)
        if (username === 'manager'){
            return <Nav className="mr-auto">
                        <Link to='/userlist' className='nav_link'><h3>Users List</h3></Link><h4>|</h4>
                        <Link to='/managelist' className='nav_link'><h3>Manage Appointments</h3></Link><h4>|</h4>
                        <Link to='/appointmentlist' className='nav_link'><h3>View Appointments</h3></Link><h4>|</h4>
                        <Link to='/manager' className='nav_link'><h3>Create Manager</h3></Link><h4>|</h4>
                        <Nav className="mr-auto"><Link to='/updateuserinfo' className='nav_link'><h3>Manage User Info</h3></Link></Nav>
                    </Nav>
    }   else if (username !== 'manager'){
            return <Nav className="mr-auto">
            <Link to='/clientprofile' className='nav_link'><h3>View Current Appointments</h3></Link><h4>|</h4>
            <Link to='/appointments' className='nav_link'><h3>Make An Appointment</h3></Link><h4>|</h4>
            <Nav className="mr-auto"><Link to='/updateuserinfo' className='nav_link'><h3>Manage User Info</h3></Link></Nav>
                    </Nav>
        }
        else{
            return <Nav className="mr-auto"></Nav>
        }
    }
    else{
        return <Nav className="mr-auto"><img src='/images/hellogif.gif' alt=''/></Nav> 
    }
}

class Routing extends Component{
    constructor(props) {
        super(props)
    }
    render(){
        return (
        <>
            <Router>
                <Navbar>
                    <Navbar.Brand><Link to='/' className='nav_link'><h1>Queen Roxxanes</h1></Link></Navbar.Brand>
                    <UserNav user={this.props.user}></UserNav>

                    <Login></Login>
                </Navbar>
                
                <Route path='/appointmentlist' component={AppointmentList}/>
                <Route path='/appointments' component={AppointmentForm}/>
                <Route path='/register' component={RegisterForm}/>
                <Route path="/login" component={Login}/>
                {/* <Route path='/managelist' component={ManageList}/> */}
                {/* <Route path='/userlist' component={UserList}/> */}
                <Route path='/clientprofile' component={ClientProfile}/>
                {/* <Route path='/manager' component={ManagerForm} /> */}
                {/* <Route path='/updateuserinfo' component={UpdateUserInfo}/> */}
            </Router>
        </>
        )
    }
}

function mapStateToProps(state) {
    const { user } = state
    return {user: user}
}

export default connect(mapStateToProps)(Routing);