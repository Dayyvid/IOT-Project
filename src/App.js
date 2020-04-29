import React, { Component } from 'react'
import './App.css'
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

class App extends Component {
  constructor () {
    super()
    this.state = {
      saturation: 0,
      brightness: 0,
      hue: 0,
      red: 0,
      green: 0,
      blue: 0,
      songName: '',
    }
    this.handleClick = this.handleClick.bind(this)
  }
  handleClick (event) {
    axios.post('http://0.0.0.0:5000/lightbulb',this.state)
      .then(response => console.log(response));
  }
  getRequest (event) {
    axios.get('http://0.0.0.0:5000/lightbulb')
      .then(response => console.log(response));
  }
  handleChange(event){
    const target = event.target;
    const value = target.value;
    const name = target.id;
    this.setState({
      [name]: value
    })
  }
  render () {
    return (
      <div>
          <Form.Group controlId="saturation" onChange={this.handleChange.bind(this)}>
            <Form.Label>Saturation</Form.Label>
            <Form.Control type="saturation" placeholder="Enter saturation" />
            <Form.Text className="text-muted">
              Enter a value between 0 to 254
            </Form.Text>
          </Form.Group>
          <Form.Group controlId="brightness" onChange={this.handleChange.bind(this)}>
            <Form.Label>Brightness</Form.Label>
            <Form.Control type="brightness" placeholder="Enter brightness" />
            <Form.Text className="text-muted">
              Enter a value between 0 to 254
            </Form.Text>
          </Form.Group>
          <Form.Group controlId="hue" onChange={this.handleChange.bind(this)}>
            <Form.Label>Hue</Form.Label>
            <Form.Control type="hue" placeholder="Enter hue" />
            <Form.Text className="text-muted">
              Enter a value between 0 to 10000
            </Form.Text>
          </Form.Group>
          <Form.Group controlId="red" onChange={this.handleChange.bind(this)}>
            <Form.Label>Red</Form.Label>
            <Form.Control type="red" placeholder="Enter red value" />
            <Form.Text className="text-muted">
              Enter a value between 0 to 255
            </Form.Text>
          </Form.Group>
          <Form.Group controlId="green" onChange={this.handleChange.bind(this)}>
            <Form.Label>Green</Form.Label>
            <Form.Control type="green" placeholder="Enter green value" />
            <Form.Text className="text-muted">
              Enter a value between 0 to 255
            </Form.Text>
          </Form.Group>
          <Form.Group controlId="blue" onChange={this.handleChange.bind(this)}>
            <Form.Label>Blue</Form.Label>
            <Form.Control type="blue" placeholder="Enter blue value" />
            <Form.Text className="text-muted">
              Enter a value between 0 to 255
            </Form.Text>
          </Form.Group>
          <Form.Group controlId="songName" onChange={this.handleChange.bind(this)}>
            <Form.Label>Song Name</Form.Label>
            <Form.Control type="songName" placeholder="Enter song name" />
            <Form.Text className="text-muted">
              Enter a song name
            </Form.Text>
          </Form.Group>
        <div className='button__container'>
          <button className='button' onClick={this.handleClick}>
            Submit
          </button>
        </div>
      </div>
    )
  }
}
export default App