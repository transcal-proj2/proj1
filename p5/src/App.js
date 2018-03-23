import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import P5Wrapper from 'react-p5-wrapper';

const p5class = require('p5')
window.p5 = new p5class()
const p = window.p5

class App extends Component {
  constructor(props){
    super(props)
    console.log(p)
    // p.createCanvas(600, 600)
    // this.p = p.bind(this)
    console.log(this)
  }

  sketch(p) {
    let rotation = 0
    let lineX = 0
 
    p.setup = function () {
      p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);
      p.frameRate(30)
    };

    p.myCustomRedrawAccordingToNewPropsHandler = function (props) {
      if (props.rotation) {
        rotation = props.rotation * Math.PI / 180;
      }
    };

    p.draw = () => {
      p.background(100);
      p.noStroke();
      p.push();
      p.rotateY(rotation);
      let b = p.box(100);
      // console.log(b)
      p.pop();
      if (p.keyIsPressed === true) {
        p.fill(0);
        p.line(lineX, 0, lineX + 100, 75)
        lineX++
        rotation += 0.1
      } else {
        p.fill(255);
      }
      p.rect(25, 25, 50, 50);
    };
  };

  render() {
    return (
      <div className="App">
        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p> */}
        <P5Wrapper sketch={this.sketch} />
      </div>
    );
  }
}

export default App;
