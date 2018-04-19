import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import P5Wrapper from 'react-p5-wrapper';

// const p = new p5
// const height = (40 * Math.round(window.innerHeight / 40))
// const width = (40 * Math.round(window.innerWidth / 40))
const height = 480
const width = 720
const s = 20


// 3.0 * Math.round(n / 3.0)


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
    this.bars = []
  }

  componentWillMount(){

  }

  componentDidMount(){
    console.log(this.p5)
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

    console.log(res.bars)
    this.bars = res.bars
  }

  sketch = (p) => {
    this.p = p
    let rotation = 0
    let lineX = 0
    let scalingFactor = 1
    let cursorX = 0
    let cursorY = 0
    let inputNodes = []
    let inputBars = []
    let nodeCount = 0
    let barCount = 0
    let selectedNode = null

    const controls = {
      view: { x: 200, y: 300, zoom: 1 },
      viewPos: { prevX: null, prevY: null, isDragging: false },
    }

    p.myCustomRedrawAccordingToNewPropsHandler = function (props) {
      if (props.rotation) {
        rotation = props.rotation * Math.PI / 180;
      }
    }

    p.keyPressed = () => {
      if (p.keyCode === p.ESCAPE) {
        selectedNode = null
      }
    }

    p.mousePressed = (e) => {
      let cellX = cursorX / 40
      let cellY = cursorY / 40 * -1

      let same = inputNodes.filter(el => {
        return el.x == cellX && el.y == cellY ? true : false
      })

      // user clicked on empty place when connecting two nodes
      if (selectedNode && same.length == 0) {
        selectedNode = null
        return
      }

      if (same.length != 0) {
        if (selectedNode) {
          inputBars.push({id: barCount, startNode: selectedNode, endNode: same[0]})
          barCount += 1
          selectedNode = null
          return
        }
        selectedNode = same[0]
      }

      
      let node = {
        n: nodeCount,
        x: cellX,
        y: cellY
      }

      nodeCount += 1

      Controls.move(controls).mousePressed(e)
      
      if (selectedNode == null) {
        setTimeout(() => {
          if (!controls.viewPos.isDragging) {
            inputNodes.push(node)
          }
        }, 200)
      }

    }

    p.mouseDragged = e => Controls.move(controls).mouseDragged(e);
    p.mouseReleased = e => Controls.move(controls).mouseReleased(e)
    
    let drawGrid = () => {
      p.stroke(200);
      p.strokeWeight(1)      
      p.fill(120)
      for (var x = -width; x < width; x += 40) {
        p.line(x, -height, x, height)
        p.text(x/40, x + 1, 12)
      }
      for (var y = -height; y < height; y += 40) {
        p.line(-width, y, width, y)
        p.text(-1 * y/40, 1, y + 12)
      }
    }

    p.setup = () => {
      p.createCanvas(width, height)
      this.setState({ canvasIsReady: true })      
    }

    p.mouseWheel = (e) => {
      // scalingFactor += ev.delta / 200
      // console.log(controls.view.zoom)
      if (controls.view.zoom > 0.5 || e.delta < 0) {
        Controls.zoom(controls).worldZoom(e)
      }
    }

    p.draw = () => {
      let z = controls.view.zoom
      p.background(240);
      p.translate(controls.view.x, controls.view.y);
      // (window.innerHeight / 40)) / 2
// const width = (40 * Math.round(window.innerWidth / 40)) / 2

      p.scale(controls.view.zoom)
      drawGrid();
      cursorX = 40 * Math.round((p.mouseX - controls.view.x) * (1 / z) / 40)
      cursorY = 40 * Math.round((p.mouseY - controls.view.y) * (1 / z) / 40)
      // p.pop()
      p.ellipse(cursorX,cursorY , 5, 5)      

      // p.translate(0, 500)   

      p.fill(0);
      this.bars.forEach(bar => {
        p.ellipse(bar.startNode.x * s, bar.startNode.y * s * -1, 5, 5)
        p.ellipse(bar.endNode.x * s, bar.endNode.y * s * -1, 5, 5)
        p.strokeWeight(1)
        p.stroke(0)
        p.line(
          bar.startNode.x * s,
          bar.startNode.y * s * -1,
          bar.endNode.x * s,
          bar.endNode.y * s * -1
        )
      })

      inputNodes.forEach(n => {
        p.ellipse(n.x * s * 2, n.y * s * -1 * 2, 5, 5)        
      })

      inputBars.forEach(b => {
        p.line(b.startNode.x * 40, b.startNode.y * 40 * -1, b.endNode.x * 40, b.endNode.y * 40 * -1)
      })

      if (selectedNode) {
        let cellX = cursorX / 40
        let cellY = cursorY / 40 * -1
        let cursorIsAboveNode = false
        let c = p.color(220, 0, 0); // Define color 'c'
        let cs = p.color(0, 255, 127); // Define color 'cs'

        p.noStroke(); // Don't draw a stroke around shapes
        
        
        for (let i = 0; i < inputNodes.length; i++) {
          if (inputNodes[i].x == cellX && inputNodes[i].y == cellY && inputNodes[i] !== selectedNode){
            cursorIsAboveNode = true
            p.fill(cs)
            p.ellipse(cursorX, cursorY, 7, 7)
          }
        }
        
        p.stroke(cursorIsAboveNode ? cs : c)
        p.line(selectedNode.x * 40, selectedNode.y * 40 * -1, cursorX, cursorY);      
        p.ellipse(selectedNode.x * 40, selectedNode.y * 40 * -1, 7, 7); // Draw left circle
      }
    }
    
  }

  render() {
    return (
      <div className="App">
        {/* <div>TrelissApp</div> */}
        <div className="p5-wrapper">
          <P5Wrapper ref={(e) => this.p5 = e}sketch={this.sketch} />
        </div>
        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p> */}
      </div>
    );
  }
}

class Controls {
  static move(controls) {
    function mousePressed(e) {
      controls.viewPos.isDragging = true;
      controls.viewPos.prevX = e.clientX;
      controls.viewPos.prevY = e.clientY;
    }

    function mouseDragged(e) {
      const { prevX, prevY, isDragging } = controls.viewPos;
      if (!isDragging) return;

      const pos = { x: e.clientX, y: e.clientY };
      const dx = pos.x - prevX;
      const dy = pos.y - prevY;

      if (prevX || prevY) {
        controls.view.x += dx;
        controls.view.y += dy;
        controls.viewPos.prevX = pos.x, controls.viewPos.prevY = pos.y
      }
    }

    function mouseReleased(e) {
      controls.viewPos.isDragging = false;
      controls.viewPos.prevX = null;
      controls.viewPos.prevY = null;
    }

    return {
      mousePressed,
      mouseDragged,
      mouseReleased
    }
  }

  static zoom(controls) {
    // function calcPos(x, y, zoom) {
    //   const newX = width - (width * zoom - x);
    //   const newY = height - (height * zoom - y);
    //   return {x: newX, y: newY}
    // }

    function worldZoom(e) {
      const { x, y, deltaY } = e;
      const direction = deltaY > 0 ? -1 : 1;
      const factor = 0.025;
      const zoom = 1 * direction * factor;



      const wx = (x - controls.view.x) / (width * controls.view.zoom);
      const wy = (y - controls.view.y) / (height * controls.view.zoom);

      controls.view.zoom += zoom;
      controls.view.x -= wx * width * zoom;
      controls.view.y -= wy * height * zoom;
            
    }
    return { worldZoom }
  }
}

export default App;
