import  React, { Component } from  'react';
import { BrowserRouter } from  'react-router-dom'
import { Route, Link } from  'react-router-dom'
import  WordsList  from  './builder/WordsList'
import  WordCreateUpdate  from  './builder/WordCreateUpdate'
import  './App.css';

var username = "";

setUsername.bind(this);

function setUsername(username) {
  this.username = username
  return username
}

const  BaseLayout  = () => (
  <div  className="container-fluid">
      <nav  className="navbar navbar-expand-lg navbar-light bg-light">
          <a  className="navbar-brand"  href="#">Build vocabulary</a>
          <button  className="navbar-toggler"  type="button"  data-toggle="collapse"  data-target="#navbarNavAltMarkup"  aria-controls="navbarNavAltMarkup"  aria-expanded="false"  aria-label="Toggle navigation">
          <span  className="navbar-toggler-icon"></span>
      </button>
      <div  className="collapse navbar-collapse"  id="navbarNavAltMarkup">
          <div  className="navbar-nav">
              <a  className="nav-item nav-link"  href="/">Words</a>
              <a  className="nav-item nav-link"  href="/builder/:pk">Add new word</a>
          </div>
      </div>
      </nav>
      <div  className="content">
          <Route  user={this.username} path="/builder/"  exact  component={WordsList} setUser={setUsername} />
          <Route  user={this.username} path="/builder/:pk"  component={WordCreateUpdate}  />
          <Route  user={this.username} path="/builder/create/"  exact  component={WordCreateUpdate}  />
      </div>
  </div>
  )

  class App extends Component {
    render() {
      return (
        <BrowserRouter>
          <BaseLayout/>
        </BrowserRouter>
      );
    }
  
  }
  
  export default App;