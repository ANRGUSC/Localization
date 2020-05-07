import React, { Component } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import ModalDropdown from 'react-native-modal-dropdown';

export default class Subscribe extends Component<{}> {
    /**
     * Record a list of channel user can select
     * value stands for the value currently selected
     * and the default selected channel is channel one
     * */
    constructor(props) {
        super(props);
        this.state = {
            value: 'one',
            options: ['one', 'two','three','four','five','six']
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    /**
     * This method is revoke when user select a value inside <Select>
     * and record the selected value in private variable "value"
     * */
    handleChange(index, value) {
        this.setState({
            value: value
        });

    }
    /**
     * This method pass the submitted value to App.js to subscribe a channel
     * */
    handleSubmit(event) {
        event.preventDefault();
        this.props.onSelectedClient(this.state.value);
    }
    render() {
        return(
            <View style={styles.subscribeContainer}>
                <View style={styles.selectContainer}>
                    <ModalDropdown
                        options={this.state.options}
                        onSelect={(idx, value) => this.handleChange(idx, value)}
                        textStyle={{fontSize: 20,}}
                        dropdownTextStyle={styles.dropdownTextStyle}
                    />
                </View>
                <View>
                    <Button
                        onPress={this.handleSubmit}
                        title="Submit"
                        style={styles.button}
                    />
                </View>
            </View>
        );
    }
}
// style sheet
const styles = StyleSheet.create({
    subscribeContainer:{
        margin: 10,
        flexDirection: 'row',
        justifyContent: 'space-between'
    },
    selectContainer: {
        padding: 6
    },
    dropdownTextStyle: {
        fontSize: 18,
        color: 'black'
    },
    button: {
        backgroundColor: 'dodgerblue',
        color: 'white',
        borderRadius: 3
    },
});
