const mqtt = require('mqtt');
const linkedinScraper = require('../services/linkedinScraper');

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


// publish i link di lavoro:
linkedinScraper.getJobLinks('', 'Catania')
    .then(links => {
        client.publish('node/jobs',
            Buffer.from(`Ecco i nuovi lavori:\r\n${links.join('\r\n\n')}`),
            { qos: 2 },
            console.log("msg published.")
        )
    })

/*
// NOTA: NON SI POSSONO RUNNARE DUE CLIENT DALLO STESSO DEVICE

client.on('message', function (topic, message) {
    //Called each time a message is received
    console.log('RICEVO MESSAGGIO DA ME STESSO:', topic, message.toString());
});

// subscribe to topic 'my/test/topic'
client.subscribe('node/jobs');
*/