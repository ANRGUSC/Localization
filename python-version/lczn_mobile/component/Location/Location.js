import React, { Component } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default class Location extends Component<{}> {
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
        return(
            <View style={styles.container}>
                <Text style={styles.item}> channel: {this.props.position.channel} </Text>
                <Text style={styles.item}> position: {this.props.position.coordinate[0]}   {this.props.position.coordinate[1]} </Text>
                <Text style={styles.item}> real location: {this.props.position.real_pos[0]}  {this.props.position.real_pos[1]}</Text>
                <Text style={styles.item}> estimate time: {this.props.position.timestamp[1] -this.props.position.timestamp[0]} s </Text>
                <Text style={styles.item}> round trip delay: {(this.state.time-this.props.position.timestamp[0]*1000)/1000} s </Text>
            </View>
        );
    }
}
// style sheet
const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        borderWidth: 1,
        borderColor: 'grey',
        borderRadius: 2
    },
    item: {
        fontSize: 10
    }
});