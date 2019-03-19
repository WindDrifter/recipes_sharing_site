import React, { useState, useEffect, useReducer } from 'react';
import PropTypes from "prop-types";
import { NavLink } from 'react-router-dom';
import {loginInitialState, loginReducer} from "../Reducers/LoginInfo";
function HeaderComponent(props){
  const [state, dispatch] = useReducer(loginReducer, loginInitialState);
  let isLogin = state.login;
  function switchToDark(){
  // TODO: add function to add dark class


  }
  function loginuser(){
    // use later
    let token =0;
    // localStorage.setItem('access_csrf_token', access_csrf_token);77
    dispatch({ type: 'login' });
  }
  function logoutuser(event){
    event.preventDefault();
    let access_csrf_token = sessionStorage.getItem("access_csrf_token");
    let refresh_csrf_token =  sessionStorage.getItem("refresh_csrf_token");
  //   fetch("/api/users/logout", {
  //   method: "POST",
  //   headers:{
  //     'Accept': 'application/json',
  //     'Content-Type': 'application/json'
  //   }
  // }).then(res => res.json()).then(response => onSetResult(response, false))
  //   .catch(error => console.error('Error:', error));
    dispatch({ type: 'logout' });
  }
  function onSetResult(response, login){
    if(login){dispatch({ type: 'login' });}
    else{
    dispatch({ type: 'logout' });}

  }
  const notLoginComponent = (<><li className="nav-item"><NavLink className="nav-link" to="/register">Register</NavLink></li>
  <li className="nav-item"><NavLink className="nav-link" to="/login">Login</NavLink></li></>);

  const LoggedinComponent = (<><li><NavLink className="nav-link" to="/">Items</NavLink></li>
  <li><a className="nav-link" onClick={logoutuser}>Logout</a> </li>

  </>);

  return (
    <header className="App-header">
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <ul className="navbar-nav nav mr-auto">
        <li className="nav-item"><NavLink className="nav-link" to="/">Home</NavLink></li>
        <li className="nav-item"><NavLink className="nav-link" to="/about">About</NavLink></li>
        {isLogin ? LoggedinComponent :notLoginComponent}

        <li><form></form> </li>
      </ul>
    </nav>
    </header>

  );

}
export default HeaderComponent;
