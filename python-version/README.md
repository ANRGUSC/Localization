# mqtt-lczn
## Structure
An overall structure of the whole project is presented below
![structure diagram](./images/structure.png?)

Workflow starts at mqtt-client which collect observaion vector and publish it in mqtt channel "localization/observation" every 60s. 

After mqtt-server receive the message, it starts the estimate process and publish the result in channel "localization/result/:channel-id". 

Then the lczn-server will receive estimate locations from mqtt-server and send it to laptop and mobile via web socket. 

Finally, we can see the result rendering in broswer or mobile app.

### mqtt-client  

**Function**: publish RF observations to mqtt-server every 60s. (fake random data read from sensor.py)

__Payload__:
1. real position(real_pos) 
2. message id(‘msg_id’)  
3. observation(3 RF obs) 
4. channel id(client id)  
5. timestamp(time of sending this request)
6. ALG(which estimate algorithm is used)

### mqtt-server 

**Function**: estimate location received from mqtt-client, and then publish estimate result . 
if mqtt-client doesn't specify estimate algorithm in the payload, it wil use MLE in default. 
> detail implementation can be found [here](./mqtt-server/README.md)

**Payload**: 
1. real position(real_pos) 
2. message id(‘msg_id’) 
3. channel id(client id)  
4. coordinate(estimate location)
5. timestamp(time of finish estimating observation)

### lczn-server 

**Function**: receive estimate location from mqtt-server, send it to browser or mobile via web socket

**Detail**: 
- record a list of clients who subscribe to certain channel. 
- On message received from mqtt-server, forward estimate result to all the clients(browser or mobile) through web socket

### lczn-client

 **Function**: visualized estimate result using [react.js](https://reactjs.org/) in browser 

**How to use**: select a channel id you wish to connect. Then browser will update itself after receiving new position.

## Floor Plan


Original Floor Plan | Modeled Floor Plan
--------------------|--------------------
![structure diagram](./images/floor.jpg)|![structure diagram](./images/model_floor.png)

 
## How to Run
### Install dependency
dependency including: node.js, react, react-native, numpy, paho-mqtt.

check instructions here. install [node.js](https://nodejs.org/en/download/)
and [pip](https://pip.pypa.io/en/stable/installing/)
 

install numpy: 
`pip install numpy`

install paho.mqtt: 
`pip install paho-mqtt`

install react: 
`npm install -g create-react-app`

install react-native:
`npm install -g create-react-native-app`

### Quick Start
Run the bash file. It will automatically set up everything for you

`bash mqtt-lczn.sh`

Click to see the example video below

[![example video](./images/sample_output.png)](https://youtu.be/Fu_UMghIy7Y)

### Run Each Service
Alternatively, you can start each service separately.

Click to see the example video below

[![example video](./images/sample_output.png)](https://youtu.be/rGWi0FtwM3Y)

`cd lczn-server`

 start service by: 
 
` $npm install `
then
`$npm start`

`cd lczn-client`
start service by:

`$npm install`
then
` $npm start`

select channel one and submit to subscribe estimate position of channel one  

`cd mqtt-server`

start service by:  

` $python mqtt-server.py`

`cd mqtt-client `

start service by:

`$python mqtt-client.py`

### How to Run Mobile Simulator

See the example video below

[![example video](./images/mobile_screenshot.png)](https://youtu.be/9rDSC9XVckM)

Installing dependencies: Node, Watchman

`brew install node`

`brew install watchman`

The React Native CLI

`npm install -g react-native-cli`

**IOS Simulator**

This simulator can only be opened in Mac environment. 

run the application by:
```
npm install 
react-native eject 
react-native link 
react-native run-ios 
```



**Android Simulator**

Follow instruction here to [Install Android Studio](https://facebook.github.io/react-native/docs/getting-started.html)

After installing dependency, an android simulator should pop up.

type in terminal to run the code:
```
npm install 
react-native eject 
react-native link 
react-native run-android 
```


**Note:** it could take a few minutes to start the service

## Sample Test output
![sample output](./images/sample_output.png)

![sample output](./images/browser_sample.png)

![sample output](./images/mobile_sample.png)


## Task List
- [x] Render estimate position using fake data
- [ ] Built fingerprinting model

> see the detail localization algorithm in Nachikethas's Paper [here](https://github.com/ANRGUSC/Lczn.jl)
