import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import P5Wrapper from 'react-p5-wrapper';

// const p = new p5

class App extends Component {
  constructor(props){
    super(props)
    this.state = {
      canvasIsReady: false
    }
    // console.log(p)
    // p.createCanvas(600, 600)
    // this.p = p.bind(this)
    console.log(this)
    this.p = null
  }

  componentWillMount(){

  }

  componentDidUpdate(prevProps, prevState, snap){
    if (this.state.canvasIsReady) {
      console.log("canvas is ready")
      this.calculate()
    }
  }

  calculate = async () => {
    let res = await fetch('http://localhost:3000/result', {})
    res = await res.json()
    console.log(res)
    // res.coordinates.nodes.forEach((node) => {
    //   console.log(node)
    //   this.p.ellipse(node.x * 100, node.y * 100, 5, 5)
    //   this.p.ellipse(200, 0, 10, 10)
    // })
    let s = 100
    console.log(res.bars)
    res.bars.forEach(bar => {
      this.p.ellipse(bar.startNode.x * s, bar.startNode.y * s, 5, 5)      
      this.p.ellipse(bar.endNode.x * s, bar.endNode.y * s, 5, 5) 
      console.log(bar.id)
      // this.p.line(
      //   bar.startNode.x * s,
      //   bar.startNode.y * s,
      //   bar.endNode.x * s,
      //   bar.endNode.y * s
      // )

    })
  }

  sketch = (p) => {
    this.p = p
    this.setState({ canvasIsReady : true })
    let rotation = 0
    let lineX = 0
 
    p.setup = function () {
      p.createCanvas(window.innerWidth, window.innerHeight, p.WEBGL);
      p.frameRate(30)
      p.stroke(0)
      p.strokeWeight(4)
    
    }

    p.myCustomRedrawAccordingToNewPropsHandler = function (props) {
      if (props.rotation) {
        rotation = props.rotation * Math.PI / 180;
      }
    }

    // p.draw = () => {
    //   let x, y
    //   p.background(100);
    //   p.noStroke();
    //   p.line(25, 25, 100, 100)   
    //   p.push();
    //   p.rotateY(rotation);
    //   let b = p.box(100);
    //   // console.log(b)
    //   p.pop();
    //   if (p.keyIsPressed === true) {
    //     p.fill(0);
    //     p.line(lineX, 0, lineX + 100, 75)
    //     lineX++
    //     rotation += 0.1
    //   } else {
    //     p.fill(255);
    //   }
    //   p.rect(25, 25, 50, 50);

    // }
    
  }

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
