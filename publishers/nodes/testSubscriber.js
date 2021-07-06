const mqtt = require('../node_modules/mqtt');

let options = {
    host: '2de97254567d4bff9dd9184c3910ace3.s1.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'iotProject',
    password: 'unTrabaj0'
}

let client = mqtt.connect(options);

client.on('connect', () => console.log('Connected'));
client.on('error', err => console.log(err));

// subscription al topic /node/jobs
const topicName = 'node/jobs'; 
client.subscribe(topicName, { qos: 2 }, () => {
    console.log(`Subscribed to topic: ${topicName}`);
});


client.on('message', function (topic, message) {
    //Called each time a message is received
    console.log('Received message:', topic, message.toString());
});