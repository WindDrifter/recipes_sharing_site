import React from 'react';
import {BrowserRouter as Router, Route} from 'react-router-dom';
import './stylesheets/App.scss';
import Register from "./MainComponents/register";
import Home from "./MainComponents/home";
import FooterComponent from "./MainComponents/footer-component";
import About from "./MainComponents/about";
import LoginComponent from "./MainComponents/login";
import HeaderComponent from "./MainComponents/header-component";

// Make FooterComponent stays next the ending dif with className app
function App(props){
    return (
      <Router>
        <div className="App">
          <HeaderComponent />
          <Route exact={true} path='/' component={Home} />
          <Route path='/register' component={Register} />
          <Route path='/about' component={About} />
          <Route path='/login' component={LoginComponent} />
          <FooterComponent />
        </div>
      </Router>
    );

}

export default App;
