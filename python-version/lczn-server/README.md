# lczn-server
## Structure
![structure](../images/lczn-server.png)
## Function
Initial a Node.js server which listens to port number 4200 in default

This component is used to combine MQTT protocol with web socket. Work as a intermediate component between mqtt-server and lczn-client.

Subscribe to a topic and distribute it to all clients through web socket
 
## Dependency
MQTT.js: work with MQTT protocol and subscribe "localization/result/"

Socket.io: work with web socket. Keep track of clients in each channel.