import React, { Component } from 'react';
import { LineChart, Line } from 'recharts';
import axios from 'axios';

export default class Graph extends Component {
	constructor(props) {
		super();
		this.state = {};
	}

	// async componentWillMount() {
	// 	let received = await axios('http://localhost:5000/api');
	// 	let data = []
	// 	received.data.data.forEach(point => { data.push({ uv: point }) })
	// 	console.log(data)
	// 	this.setState({ 'json': data });
	// 	console.log(this.state.json)
	// }

	blank = async() => {
		let received = await axios('http://localhost:5000/api');
		let data = []
		received.data.data.forEach(point => { data.push({ uv: point }) })
		console.log(data)
		this.setState({ 'blank': data });
	}

	measure = async() => {
		let received = await axios.post('http://localhost:5000/blank', this.state.calibration);
		let data = []
		received.data.data.forEach(point => { data.push({ uv: point }) })
		console.log(data)
		this.setState({ 'json': data });
		console.log(this.state.json)
	} // TODO: COLOR CALIBRATION
	
	calibrate = async() => {
		alert('Shine frequency 1 as you click OK')
		let c1 = await axios('http://localhost:5000/calibrate');
		alert('Shine frequency 2 as you click OK')
		let c2 = await axios('http://localhost:5000/calibrate');
		alert('Shine frequency 3 as you click OK')
		let c3 = await axios('http://localhost:5000/calibrate');

		this.setState({ 'calibration': [[c1.maxPixel, 450], [c2.maxPixel, 550], [c3.maxPixel, 650]] });
	}

	render() {
		return (
			<div>
				<LineChart width={window.innerWidth} height={window.innerHeight} data={this.state.json}>
					<Line type="monotone" dataKey="uv" stroke="#8884d8" />
				</LineChart>
				<button onClick={this.blank}>Blank</button>
				<button onClick={this.calibrate}>Calibrate</button>
				<button onClick={this.measure}>Measure</button>
			</div>
		);
	}
}