import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';

import HelloWorld from "./components/hello";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { };
  }

  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route
            exact
            path="/"
            render={() => <HelloWorld state={this.state} />}
          />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;