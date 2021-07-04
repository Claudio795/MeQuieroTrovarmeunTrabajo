var mqtt = require('mqtt')

var options = {
    host: '2de97254567d4bff9dd9184c3910ace3.s1.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'iotProject',
    password: 'unTrabaj0'
}

//initialize the MQTT client
var client = mqtt.connect(options);

//setup the callbacks
client.on('connect', function () {
    console.log('Connected');
});

client.on('error', function (error) {
    console.log(error);
});

client.on('message', function (topic, message) {
    //Called each time a message is received
    console.log('Received message:', topic, message.toString());
});

// subscribe to topic 'my/test/topic'
client.subscribe('my/test/topic');

// publish message 'Hello' to topic 'my/test/topic'
client.publish('my/test/topic', 'Ciao Claudio');