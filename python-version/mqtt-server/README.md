# mqtt-server
## MQTT Usage

### Create a client instance
Client Constructor Example

```
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
```

### Connect to broker

Connect Example

`connect(host, port=1883, keepalive=60, bind_address="")`

The connect() function connects the client to a broker. This is a blocking function. It takes the following arguments:

**host** 
 
hostname or IP address of the remote broker

**port**

network port of the server host to connect to. Defaults to 1883. Note that the default port for MQTT over SSL/TLS is 8883 so if you are using tls_set() or tls_set_context(), the port may need providing manually

**keepalive** 
 
maximum period in seconds allowed between communications with the broker. If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker

**Callback** 

When the client receives a CONNACK message from the broker in response to the connect it generates an on_connect() callback.

### Network loop
These functions are the driving force behind the client. If they are not called, incoming network data will not be processed and outgoing network data may not be sent in a timely fashion. 

loop_forever(): This is a blocking form of the network loop and will not return until the client calls disconnect(). It automatically handles reconnecting.
                

Example:

`loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)`


### Publishing
Send a message from the client to the broker.

publish()

`publish(topic, payload=None, qos=0, retain=False)`

This causes a message to be sent to the broker and subsequently from the broker to any clients subscribing to matching topics. It takes the following arguments:

**topic**

the topic that the message should be published on

**payload** 

the actual message to send. If not given, or set to None a zero length message will be used. Passing an int or float will result in the payload being converted to a string representing that number. If you wish to send a true int/float, use struct.pack() to create the payload you require

**qos**

the quality of service level to use


**callback (publish)**

Called when a message that was to be sent using the publish() call has completed transmission to the broker.

on_publish() Example

`on_publish(client, userdata, mid)`

### Subscribe 

subscribe()

Subscribe the client to one or more topics.

`subscribe(topic, qos=0)`

**topic**

a string specifying the subscription topic to subscribe to.

**qos**

the desired quality of service level for the subscription. Defaults to 0.

**Callback (subscribe)**

When the broker has acknowledged the subscription, an on_subscribe() callback will be generated.

## Estimate Process
![estimate structure](../images/estimate.png?)

An illustration of the estimate process inside mqtt-server is stated in above. 

The localization algorithm takes three inputs: distribution of observations, prior distribution and observation vector. 

In our simulation, distribution of observations is simple path loss model or fingerprinting based model; 

prior distribution is a pre-defined matrix obtained by floor plan of EEB building; 

observation vector is a RSS vector received.

### cost function
![cost function](../images/cost.png?)

### algorithm procedure
![procedure](../images/procedure.png?)


### Sample Example for FingerPrinting

file "RSS_Location" is organized as follow:

column 1: mac address

column 2: RSS

column 3: measured position

sample table of likelihood is displyed as follow

![table of likelihood](../images/tableOfLikelihood.png)

```
obs = [-79, -84, -83, -84, -68,-77, -73, -85, -63, -62] #real position (26, 94)
print estimate(obs,'MLE') # estimate position (26, 93)
```

### Known Issue for FingerPrinting

- database is not large enough to cover all hallway area
- database is different between day and night. No uniform likelihood data for estimation