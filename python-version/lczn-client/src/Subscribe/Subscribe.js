import React, { Component } from 'react';
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import { Panel, Form, FormGroup, OverlayTrigger, Popover} from 'react-bootstrap';
import './Subscribe.css';

class Subscribe extends Component {
    /**
     * Record a list of channel user can select
     * value stands for the value currently selected
     * and the default selected channel is channel one
     * */
    constructor(props) {
        super(props);
        this.state = {
            value: 'one',
            options: [
                { value: 'one', label: 'One', className: 'client' },
                { value: 'two', label: 'Two', className: 'client' },
                { value: 'three', label: 'Three', className: 'client' },
                { value: 'four', label: 'Four', className: 'client' },
                { value: 'five', label: 'Four', className: 'client' },
                { value: 'six', label: 'Four', className: 'client' }
            ]
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    /**
     * This method is revoke when user select a value inside <Select>
     * and record the selected value in private variable "value"
     * */
    handleChange(option) {
        // console.log("Selected Channel: " + JSON.stringify(option.value));
        this.setState({
            value: option.value
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
        const popoverHoverFocus = (
            <Popover id="popover-trigger-hover-focus" title="alert">
                <strong>select which client you want to track!</strong>
            </Popover>
        );
        return (
            <Panel className="subscribe">
                <Form inline onSubmit={this.handleSubmit}>
                    <label> Select Channel Name: </label>
                    {' '}
                    <FormGroup>
                            <Select
                                name="subscribe-form-select-name"
                                clearable={false}
                                value={this.state.value}
                                options={this.state.options}
                                onChange={this.handleChange}
                            />
                    </FormGroup>

                    <OverlayTrigger trigger={['hover', 'focus']} placement="bottom" overlay={popoverHoverFocus}>
                        <input type="submit" value="Submit" className="subscribe-form-submit"/>
                    </OverlayTrigger>

                </Form>
            </Panel>
        );
    }
}

export default Subscribe;