import React from 'react';


class HelloWorld extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      helloWorld: null,
    };
  }

  componentDidMount() {
    this.getHello();
  }

  getHello() {
    fetch('http://127.0.0.1:7000/api/')
      .then((response) => response.json())
      .then((json) => {
        this.setState({
          helloWorld: json['message']
        });
        this.forceUpdate();
      })
      .catch(() => {
      });
  }

  render() {
    return (
      <div>
        <h4>{this.state.helloWorld}</h4>
      </div>
    );
  }
}

export default HelloWorld;