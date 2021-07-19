const mqtt = require('../node_modules/mqtt');
const mqttOptions = require('../brokerConnectionEnv');
const getNews = require('../services/googleNews');
const CronJob = require('../node_modules/cron').CronJob;

let client = mqtt.connect(mqttOptions);

// TODO: CronJob per ora è 1 messaggio ogni minuto; da cambiare con "ogni 4 ore" (= 240 minuti)
const job = new CronJob('0 */1 * * * *', async () => {
    let news = await getNews();
    client.publish('node/news',
        Buffer.from(`Ecco le notizie:\r\n${news.join('\r\n\n')}`),
        { qos: 1, retain: true },
        console.log("news msg published.")
    )
});

client.on('connect', () => { 
    console.log('Connected');
    job.start();
});
client.on('error', err => console.log(err));

/** TEST
client.subscribe('node/news');
client.on("message", (topic, msg) => console.log(`news msg: ${msg}`));
*/