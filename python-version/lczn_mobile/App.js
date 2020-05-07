/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import { View, Text, ListView, FlatList, ListItem, StyleSheet } from 'react-native';
import io from 'socket.io-client';
import Floor from './component/Floor/Floor';
import Subscribe from './component/Subscribe/Subscribe';
import Location from './component/Location/Location';

export default class App extends Component<{}> {
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
    }
    /**
     * This function used to select channel number and subscribe to lczn-server through web socket
     * and reset history data when subscribe to other channel
     * */
    handleSelectedClient(client) {
        alert("inside app.js selected " + client);
        this.setState({
            clientID: client,
            positions: null,
            deltaP: null,
            deltaR: null
        });
        const socket = io('http://localhost:4200', { query: 'subscribe='+client});
        socket.on('message', (message) => {
            let position = JSON.parse(message);
            this.setState({
                positions: this.state.positions? this.state.positions.concat(position) : new Array(position),
                deltaP: position.coordinate,
                deltaR: position.real_pos
            });
        });
    }

    render() {
            return (
                <View style={styles.container}>
                    <Subscribe onSelectedClient = {this.handleSelectedClient}/>
                    <Floor deltaP = {this.state.deltaP} deltaR = {this.state.deltaR}/>
                    <FlatList
                        data={this.state.positions}
                        renderItem={({item}) => <Location position={item} key={JSON.stringify(item)}/>}
                    />
                </View>
            );

    }
}
// style sheet
const styles = StyleSheet.create({
    container:{
        flexDirection: 'column',
        justifyContent: 'center',
        padding: 40
    }
});
