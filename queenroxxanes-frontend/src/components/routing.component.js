import React, { Component } from 'react';
import { Route, BrowserRouter as Router, Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import { connect } from 'react-redux'

import RegisterForm from './register.component';
import Login from './login.component';
import '../sass/nav.scss';


function UserNav(props) {
    const UserLoggedIn = props.user
    if (UserLoggedIn && 'role' in UserLoggedIn) {
        let role = UserLoggedIn.role
        role = role.toUpperCase()
        console.log('has a role')
        console.log(UserLoggedIn.role)
        if (role === 'MANAGER'){
            return <Nav className="mr-auto">
                        <Link to='/userlist' className='nav_link'><h3>Users List</h3></Link><h4>|</h4>
                        <Link to='/managelist' className='nav_link'><h3>Manage Auctions</h3></Link><h4>|</h4>
                        <Link to='/productlist' className='nav_link'><h3>View Products</h3></Link><h4>|</h4>
                        <Link to='/employee' className='nav_link'><h3>Create Employee</h3></Link><h4>|</h4>
                        <Nav className="mr-auto"><Link to='/updateuserinfo' className='nav_link'><h3>Manage User Info</h3></Link></Nav>
                    </Nav>
        } else if (role === 'AUCTIONEER'){
            return <Nav className="mr-auto">
                        <Link to='/managelist' className='nav_link'><h3>Manage Auction</h3></Link><h4>|</h4>
                        <Nav className="mr-auto"><Link to='/updateuserinfo' className='nav_link'><h3>Manage User Info</h3></Link></Nav>
                    </Nav>
        } else {//(UserLoggedIn.role.toUpper() === 'CURATOR'){
            /*Need to see a list of products without the accept/deny buttons*/
            return <Nav className="mr-auto">
                        <Link to='/products' className='nav_link'><h3>Product Proposal</h3></Link><h4>|</h4>
                        {/* <Link to='/productlist' className='nav_link'><h3>View Products</h3></Link><h4>|</h4> */}
                        <Nav className="mr-auto"><Link to='/updateuserinfo' className='nav_link'><h3>Manage User Info</h3></Link></Nav>
                    </Nav>     
        }
    }
    else if (UserLoggedIn && 'history' in UserLoggedIn){
        return <Nav className="mr-auto">
                    <Link to='/bidderprofile' className='nav_link'><h3>View History</h3></Link><h4>|</h4>
                    <Link to='/auctionlist' className='nav_link'><h3>Auctions</h3></Link><h4>|</h4>
                    <Nav className="mr-auto"><Link to='/updateuserinfo' className='nav_link'><h3>Manage User Info</h3></Link></Nav>
                </Nav>
    } 
    else {
        return <Nav className="mr-auto"></Nav>
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
                
                <Route path='/register' component={RegisterForm}/>
                <Route path="/login" component={Login}/>
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