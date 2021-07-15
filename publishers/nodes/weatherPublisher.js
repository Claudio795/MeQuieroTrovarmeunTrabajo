const mqtt = require('../node_modules/mqtt');
const mqttOptions = require('../brokerConnectionEnv');
const getWeather = require('../services/weather');

let client = mqtt.connect(mqttOptions);

client.on('connect', () => console.log('Connected'));
client.on('error', err => console.log(err));

// al ricevimento dei dati quali coordinate gps e tipo di lavoro, si avvia la ricerca:
client.on('message', async (topic, msg) => {
    let parsedMsg = await JSON.parse(msg);
    console.log(parsedMsg);

    let lat = parseFloat(parsedMsg.lat) + 0.00000001;
    let lon = parseFloat(parsedMsg.lon) + 0.00000001;

    getWeather(lat, lon).then(weatherInfo => {
        client.publish('node/weather',
            Buffer.from(`Ecco il meteo:\r\n${weatherInfo.join('\r\n\n')}`),
            { qos: 2 },
            console.log("weather msg published.")
        )
    });
});
// sottoscrizione al topic /user/info -> nome del topic modificabile a piacere
client.subscribe('user/info');


/** TEST
client.subscribe('node/weather');
*/

/** Esempio:
setTimeout(() => {
    getWeather('catania').then(weatherInfo => {
        client.publish('node/weather',
            Buffer.from(`Ecco il meteo:\r\nTemperatura: ${weatherInfo[0]} °C\r\nPrevisione: ${weatherInfo[1]}`),
            { qos: 2 },
            console.log("weather msg published.", weatherInfo)
        )
    });
}, 2500);

client.on('message', function (topic, message) {
    //Called each time a message is received
    console.log('Received message:', topic, message.toString());
});
*/