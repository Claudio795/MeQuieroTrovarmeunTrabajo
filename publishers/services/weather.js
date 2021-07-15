const fs = require("fs");
const key = fs.readFileSync("../openWeatherAPI.key");
const unirest = require("../node_modules/unirest");

const language = 'it';

const getWeather = (lat, lon) => {
    return new Promise((res, rej) => {
        let cityWeather = unirest.get(`http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${key}&lang=${language}`);
        res(cityWeather)
    }).then(res => {
        return [
            parseInt(res.body.main.temp - 273), // la temperatura la si ottiene in Kelvin
            res.body.weather[0].description // weather è un array con un solo elemento
        ];
    })
}

module.exports = getWeather;

/** Esempio
getWeather("Sant'Agata Li Battiati").then(res => {
    let info = res;
    console.log(info);
});
*/