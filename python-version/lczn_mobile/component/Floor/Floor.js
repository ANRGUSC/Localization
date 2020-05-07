import React, { Component } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import ChartView from 'react-native-highcharts';

export default class Floor extends Component<{}> {
    /**
     * this.state.config record office area outline, estimate location and real location
     * you can customize the title, width & color of the line in this attribute*/
    constructor(props) {
        super(props);
        this.state = {
            config: {
                chart: {
                    type: 'spline',
                    marginRight: 100,
                },
                title: {
                    text: 'Real Time Position Tracking'
                },
                xAxis: {
                    title: {
                        enabled: true,
                        text: 'Width'
                    },
                    gridLineWidth: 1
                },
                yAxis: {
                    title: {
                        text: 'Height'
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: 'position: [{point.x} , {point.y}]'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },
                exporting: {
                    enabled: true
                },
                series: [{
                    name: 'Office Area1',
                    data: [[0, 0], [6, 0], [6, 48], [0, 48],[0,0]],
                    enableMouseTracking: false,
                },{
                    name: 'Office Area2',
                    data: [[10, 0], [53, 0], [53, 6], [10, 6], [10, 0]],
                    enableMouseTracking: false
                },{
                    name: 'Office Area3',
                    data: [[10, 10], [22, 10], [22, 48], [10, 48],[10, 10]],
                    enableMouseTracking: false
                },{
                    name: 'Office Area4',
                    data: [[29, 10], [53, 10], [53, 94], [29, 94], [29, 10]],
                    enableMouseTracking: false
                },{
                    name: 'Office Area5',
                    data: [[0, 53], [22, 53], [22, 90],[15,90],[15,94], [0, 94], [0, 53]],
                    enableMouseTracking: false
                },{
                    name: 'Estimate Location',
                },{
                    name: 'Real Location',
                }]
            }
        }
    }
    /**
     * this method is invoked before a mounted component receives new props.
     * Add Point to the chart using nextProps
     * nextProps.deltaP is estimate location
     * nextProps.deltaR is real location
     * */
    componentWillReceiveProps(nextProps) {
        let series1 = this.state.config.series[5];
        if(nextProps.deltaP) {
            if(typeof(series1.data) === "undefined") {
                series1.data = new Array();
                series1.data[0] = new Array(nextProps.deltaP[0],nextProps.deltaP[1]);
            } else {
                let len = series1.data.length;
                series1.data[len] = new Array(nextProps.deltaP[0],nextProps.deltaP[1]);
            }
        }
        let series2 = this.state.config.series[6];
        if(nextProps.deltaR) {
            if(typeof(series2.data) === "undefined") {
                series2.data = new Array();
                series2.data[0] = new Array(nextProps.deltaR[0],nextProps.deltaR[1]);
            } else {
                let len = series2.data.length;
                series2.data[len] = new Array(nextProps.deltaR[0],nextProps.deltaR[1]);
            }
        }
    }

    render() {
        return (
            <View>
                <ChartView style={{height:300}} config={this.state.config}></ChartView>
            </View>
        );
    }
}