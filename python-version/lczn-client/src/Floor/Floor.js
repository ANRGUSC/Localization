import React, { Component } from 'react';
import './Floor.css';
import ReactHighcharts from 'react-highcharts';
// Highcharts more
var HighchartsMore = require('highcharts-more');
HighchartsMore(ReactHighcharts.Highcharts);
// Highcharts exporting
var HighchartsExporting = require('highcharts-exporting');
HighchartsExporting(ReactHighcharts.Highcharts);

class Floor extends Component {
    /**
     * this method is invoked before a mounted component receives new props.
     * Add Point to the chart using nextProps
     * nextProps.deltaP is estimate location
     * nextProps.deltaR is real location
     * */
    componentWillReceiveProps(nextProps) {
        let chart = this.refs.chart.getChart();
        if(nextProps.deltaP) {
            chart.series[0].addPoint({x: nextProps.deltaP[0], y: nextProps.deltaP[1]});
        }
        if(nextProps.deltaR) {
            chart.series[1].addPoint({x: nextProps.deltaR[0], y: nextProps.deltaR[1]});
        }
    }
    /**
     * this.state.config record office area outline, estimate location and real location
     * you can customize the title, width & color of the line in this attribute*/
    constructor(props) {
        super(props);
        this.state = {
            config: {
                title: {
                    text: 'Real Time Position Tracking'
                },
                xAxis: {
                    gridLineWidth: 1,
                    title: {
                        enabled: true,
                        text: 'Width'
                    },
                    startOnTick: true,
                    endOnTick: true,
                    showLastLabel: true
                },
                yAxis: {
                    title: {
                        text: 'Height'
                    }
                },
                plotOptions: {
                    series: {
                        lineWidth: 2,
                        lineColor:'#000000'
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },
                series: [
/*
		{
                    name: 'Office Area1',
                    type: 'polygon',
                    data: [[0, 0], [6, 0], [6, 48], [0, 48],[0, 0]],
                    color: ReactHighcharts.Highcharts.Color(ReactHighcharts.Highcharts.getOptions().colors[0]).setOpacity(0.5).get(),
                    enableMouseTracking: false
                }, {
                    name: 'Office Area2',
                    type: 'polygon',
                    data: [[10, 0], [53, 0], [53, 6], [10, 6], [10, 0]],
                    color: ReactHighcharts.Highcharts.Color(ReactHighcharts.Highcharts.getOptions().colors[0]).setOpacity(0.5).get(),
                    enableMouseTracking: false
                }, {
                    name: 'Office Area3',
                    type: 'polygon',
                    data: [[10, 10], [22, 10], [22, 48], [10, 48],[10, 10]],
                    color: ReactHighcharts.Highcharts.Color(ReactHighcharts.Highcharts.getOptions().colors[0]).setOpacity(0.5).get(),
                    enableMouseTracking: false
                }, {
                    name: 'Office Area4',
                    type: 'polygon',
                    data: [[29, 10], [53, 10], [53, 94], [29, 94], [29, 10]],
                    color: ReactHighcharts.Highcharts.Color(ReactHighcharts.Highcharts.getOptions().colors[0]).setOpacity(0.5).get(),
                    enableMouseTracking: false
                },{
                    name: 'Office Area5',
                    type: 'polygon',
                    data: [[0, 53], [22, 53], [22, 90],[15,90],[15,94], [0, 94], [0, 53]],
                    color: ReactHighcharts.Highcharts.Color(ReactHighcharts.Highcharts.getOptions().colors[0]).setOpacity(0.5).get(),
                    enableMouseTracking: false
                }, 
*/
		{
                    name: 'Estimate Location',
                    type: 'scatter',
                    color: ReactHighcharts.Highcharts.getOptions().colors[2],
                    lineColor:ReactHighcharts.Highcharts.getOptions().colors[2],
                    data: []
                }, {
                    name: 'Sensor Location',
                    type: 'scatter',
                    color: ReactHighcharts.Highcharts.getOptions().colors[3],
                    lineColor:ReactHighcharts.Highcharts.getOptions().colors[3],
                    data: []
                }],
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: 'position: [{point.x} , {point.y}]'
                }
            }
        }
    }


    render() {
        return (
            <div className="Floor">
                <ReactHighcharts config = {this.state.config} ref="chart"> </ReactHighcharts>
            </div>
        );
    }
}

export default Floor;
