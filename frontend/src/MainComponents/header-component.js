import React, { useState, useEffect, useReducer } from 'react';
import PropTypes from "prop-types";
import { NavLink } from 'react-router-dom';
import { connect } from "react-redux";
import {LOGIN, LOGOUT} from "../constants/action-constants";

function mapDispatchToProps(dispatch) {
  return {
    loginuser: ()=> dispatch({ type: LOGIN}),
    logoutuser: ()=> dispatch({ type: LOGOUT})
  };
}
const mapStateToProps = state => {
  return { login: state.login };
};
function HeaderConnect(props){
  function switchToDark(){
  // TODO: add function to add dark class


  }
  function loginuser(){
    // use later
    // localStorage.setItem('access_csrf_token', access_csrf_token);77
  }
  function logoutuser(event){
    event.preventDefault();
    let access_csrf_token = sessionStorage.getItem("access_csrf_token");
    // let refresh_csrf_token =  sessionStorage.getItem("refresh_csrf_token");

    fetch("/api/users/logout", {
    method: "POST",
    headers:{
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      "X-CSRF-TOKEN": access_csrf_token
    }
  }).then(res => res.json()).then(response => onSetResult(response, false))
    .catch(error => console.error('Error:', error));
  }
  function onSetResult(response, login){
    if(login){
      props.loginuser();

    }
    else{
      props.logoutuser();
      sessionStorage.clear();
    }

  }
  const notLoginComponent = (<><li className="nav-item"><NavLink className="nav-link" to="/register">Register</NavLink></li>
  <li className="nav-item"><NavLink className="nav-link" to="/login">Login</NavLink></li></>);

  const loggedinComponent = (<><li><NavLink className="nav-link" to="/">Posts</NavLink></li>
  <li><a className="nav-link" onClick={logoutuser}>Logout</a> </li>

  </>);
  return (
    <header className="App-header">
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <ul className="navbar-nav nav mr-auto">
        <li className="nav-item"><NavLink className="nav-link" to="/">Home</NavLink></li>
        <li className="nav-item"><NavLink className="nav-link" to="/about">About</NavLink></li>
        { props.login ? loggedinComponent :notLoginComponent}

        <li><form></form> </li>
      </ul>
    </nav>
    </header>

  );

}
const HeaderComponent = connect(mapStateToProps, mapDispatchToProps)(HeaderConnect);
export default HeaderComponent;
