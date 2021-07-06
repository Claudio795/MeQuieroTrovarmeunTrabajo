const mqtt = require('mqtt');
const linkedinScraper = require('../services/linkedinScraper');
const getNearestCity = require('../services/nearestCity').getNearestCity;

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


// publish i link di lavoro
// al ricevimento dei dati quali coordinate gps e tipo di lavoro, si avvia la ricerca:
client.on('message', async (topic, msg) => {
    let parsedMsg = await JSON.parse(msg);
    console.log(parsedMsg);

    let lat = parseFloat(parsedMsg.lat) + 0.00000001;
    let lon = parseFloat(parsedMsg.lon) + 0.00000001;
    
    let qualification = await parsedMsg.qualification;
    let city = await getNearestCity(lat, lon);

    await linkedinScraper.getJobLinks(qualification, city)
    .then(links => {
        client.publish('node/jobs',
            Buffer.from(`Ecco i nuovi lavori:\r\n${links.join('\r\n\n')}`),
            { qos: 2 },
            console.log("msg published.")
        )
    })

});

// sottoscrizione al topic /user/info -> nome del topic modificabile a piacere
client.subscribe('user/info');