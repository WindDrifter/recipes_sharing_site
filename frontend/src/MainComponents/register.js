import React, { useState } from 'react';
import PropTypes from "prop-types";
import {withRouter} from "react-router";
import "../stylesheets/register.scss";
function Register(props) {
  // Declare a new state variable, which we'll call "count"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword]= useState("");
  const [passwordConfirmation, setPasswordConfirmation]= useState("");
  function handleSubmit(event){
    event.preventDefault();

    let send_data = {name: name, email: email, username: username,
                     password: password, password_confirmation: passwordConfirmation};
    fetch("/api/users", {
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
      props.history.push("/");
  }

  return (
    <div className="align-middle mx-auto container d-flex justify-content-center align-items-center">

      <form className="form-element" onSubmit={handleSubmit}>
        <h1 className="">Registration</h1>
        <div className="form-group form-label">
          <label htmlFor="name">
            Name:
          </label>
          <input id="name" className="form-control" type="text" value={name}
          onChange={e => setName(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <label htmlFor="username">
            Username:
          </label>
          <input id="username" className="form-control" type="text" name="username" value={username}
            onChange={e => setUsername(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <label htmlFor="email">
            Email:
          </label>
          <input id="email" className="form-control" type="email" name="email" value={email}
            onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <label htmlFor="password" >
            Password:
          </label>
          <input id="password" className="col-12 form-control" type="password" name="password" value={password}
              onChange={e => setPassword(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <label htmlFor="passwordConfirmation" >
            Password Confirmation:
          </label>
          <input id="passwordConfirmation" className="col-12 form-control" type="password" name="password" value={passwordConfirmation}
              onChange={e => setPasswordConfirmation(e.target.value)} />
        </div>
        <div className="form-group form-label">
          <input className="col-12 form-control" type="submit" value="Submit" />
        </div>
      </form>
    </div>
  );
}
export default Register;
