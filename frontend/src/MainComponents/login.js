import React, { useState } from 'react';
import {withRouter} from "react-router";
import "../stylesheets/register.scss";
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
function LoginForm(props) {
  // Declare a new state variable, which we'll call "count"
  const [username, setUsername] = useState("");
  const [password, setPassword]= useState("");
  function handleSubmit(event){
    event.preventDefault();

    let send_data = {username: username,
                     password: password};
    fetch("/api/users/login", {
    method: "POST",
    body: JSON.stringify(send_data),
    headers:{
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    }).then(res => res.json()).then(response => onSetResult(response))
    .catch(error => console.error('Error:', error));
  }
  function onSetResult(result){
    sessionStorage.setItem("access_csrf_token", result.access_csrf_token);
    sessionStorage.setItem("refresh_csrf_token", result.refresh_csrf_token);
    sessionStorage.setItem("login", result.login);
    props.loginuser();
    props.history.push("/");
  }

  return (
    <div className="align-middle mx-auto container d-flex justify-content-center align-items-center">

      <form className="form-element" onSubmit={handleSubmit}>
        <h1 className="">Login</h1>
        <div className="form-group form-label">
          <label htmlFor="username">
            Username:
          </label>
          <input id="username" className="form-control" type="text" name="username" value={username}
            onChange={e => setUsername(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <label htmlFor="password" >
            Password:
          </label>
          <input id="password" className="col-12 form-control" type="password" name="password" value={password}
              onChange={e => setPassword(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <input className="col-12 form-control" type="submit" value="Submit" />
        </div>
      </form>
    </div>
  );
}
const LoginComponent = connect(mapStateToProps, mapDispatchToProps)(LoginForm);

export default LoginComponent;
