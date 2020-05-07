/*
* This class is used to render a cell of message
* Including estimate position, real position and round trip delay
* */


import React, { Component } from 'react';
import { Panel } from 'react-bootstrap';

class Location extends Component {
    /**
     * Record the time when this component is created
     * */
    constructor() {
        super();
        this.state = {
            time: null
        }
    }
    /**
     * Update the time only when this component is created
     * */
    componentWillMount() {
        if(this.state.time == null) {
            this.setState({
                time: new Date().getTime()
            });
        }
    }
    /**
     * render a list of information we needed, including
     * the channel number
     * the estimate location
     * the real location
     * the time mqtt-server used to estimate the location
     * round trip delay of the whole process*/
    render() {
        return (
            <Panel className="location-group-item">
                <div className="location-estimate-method">
                    channel: {this.props.position.channel}
                </div>
                <div className="location-coordinate">
                    position: {this.props.position.coordinate[0]}
                    {' '}
                    {this.props.position.coordinate[1]}
                </div>
                <div className="location-real-pos">
                    sensor location: {this.props.position.real_pos[0]}
                    {' '}
                    {this.props.position.real_pos[1]}
                </div>
                <div className="location-estimate-time">
                    estimate time: {this.props.position.timestamp[1] -this.props.position.timestamp[0]} s
                </div>
                <div className="location-round-trip-delay">
                    round trip delay: {(this.state.time-this.props.position.timestamp[0]*1000)/1000} s
                </div>
            </Panel>
        );

    }
}

export default Location;
