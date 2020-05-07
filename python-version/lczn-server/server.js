var express = require('express');
var app = express();
var http = require('http');

var socket_io = require('socket.io');
var io = socket_io();
var mqtt = require('mqtt');
var client  = mqtt.connect('mqtt://127.0.0.1');
var mqttService = require('./services/MqttService')(client, io);

var server = http.createServer(app);
io.attach(server);
server.listen(4200);
