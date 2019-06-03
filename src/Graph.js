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

	calibrate = () => {
		let received = await axios('http://localhost:5000/api');
		let data = []
		received.data.data.forEach(point => { data.push({ uv: point }) })
		console.log(data)
		this.setState({ 'calibration': data });
	}

	measure = () => {
		let received = await axios.post('http://localhost:5000/calibrated', this.state.calibration);
		let data = []
		received.data.data.forEach(point => { data.push({ uv: point }) })
		console.log(data)
		this.setState({ 'json': data });
		console.log(this.state.json)
	}

	render() {
		return (
			<div>
				<LineChart width={window.innerWidth} height={window.innerHeight} data={this.state.json}>
					<Line type="monotone" dataKey="uv" stroke="#8884d8" />
				</LineChart>
				<button onClick={this.calibrate}>Calibrate</button>
				<button onClick={this.measure}>Measure</button>
			</div>
		);
	}
}