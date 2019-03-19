import React, { Component } from 'react';
import {BrowserRouter as Router, Route, Link} from 'react-router-dom';
import logo from './logo.svg';
import './stylesheets/App.scss';
import Register from "./MainComponents/register";
import Home from "./MainComponents/home";
import FooterComponent from "./MainComponents/footer-component";
import About from "./MainComponents/about";
import Login from "./MainComponents/login";

import HeaderComponent from "./MainComponents/header-component";
// Make FooterComponent stays next the ending dif with className app
class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <HeaderComponent />
          <Route exact={true} path='/' component={Home} />
          <Route path='/register' component={Register} />
          <Route path='/about' component={About} />
          <Route path='/login' component={Login} />

          <FooterComponent />
        </div>
      </Router>
    );
  }
}

export default App;
