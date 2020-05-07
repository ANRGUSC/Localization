import React, { Component } from 'react';
import io from 'socket.io-client';
import Subscribe from '../Subscribe/Subscribe';
import Floor from '../Floor/Floor.js';
import Location from '../Location/Location';
import { Panel } from 'react-bootstrap';
import './App.css';

class App extends Component {
    /**
     * Initial private variables including:
     * clientID: channel number
     * positions: list of messages receive
     * deltaP: predict position
     * deltaR: real position*/
    constructor() {
        super();
        this.state = {
            clientID: null,
            positions: null,
            deltaP: null,
            deltaR: null
        };
        this.handleSelectedClient = this.handleSelectedClient.bind(this);
        this.renderPositions = this.renderPositions.bind(this);
    }

    /**
     * This function used to select channel number and subscribe to lczn-server through web socket
     * and reset history data when subscribe to other channel
     * */
    handleSelectedClient(client) {
        console.log("inside app.js selected " + client);
        // reset to initial state
        this.setState({
            clientID: client,
            positions: null,
            deltaP: null,
            deltaR: null
        });
        const socket = io('http://'+ window.location.hostname + ':4200', { query: 'subscribe='+client});
        // update private variable when received new message
        socket.on('message', (message) => {
            let position = JSON.parse(message);
            this.setState({
                positions: this.state.positions? this.state.positions.concat(position) : new Array(position),
                deltaP: position.coordinate,
                deltaR: position.real_pos
            });
            // console.log(this.state.positions);
        });

    }
    /**
     * This piece of code used to render a list of messages received,
     * including round trip delay,  real location and  estimate location of each message*/
    renderPositions() {
        let position_list = this.state.positions.map(function(position) {
            return( <Location position={position} key={JSON.stringify(position)}/>);
        });

        return(
            <div>
                {position_list}
            </div>
        );
    }
    render() {
        if(this.state.positions) {
            return (
                <div className="App">
                    <Subscribe onSelectedClient = {this.handleSelectedClient} />
                    <Floor deltaP = {this.state.deltaP} deltaR = {this.state.deltaR}/>
                    {this.renderPositions()}

                </div>
            );
        } else {
            return (
                <div className="App">
                    <Subscribe onSelectedClient = {this.handleSelectedClient} />
                    <Floor deltaP = {this.state.deltaP} deltaR = {this.state.deltaR}/>
                    <Panel>
                        Waiting for result
                    </Panel>

                </div>
            );
        }
    }
}

export default App;
