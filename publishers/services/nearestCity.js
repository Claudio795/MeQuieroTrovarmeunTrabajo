const nearestStations = require('../node_modules/find-nearest-cities');

const maxDistance = 25000; // raggio di 25 Km
const maxResults = 3;

const nearCity = async (lat, lon) => {
    let city = JSON.parse(JSON.stringify(await nearestStations(lat, lon, maxDistance, maxResults)));
    return `${city[0].name}`;
}

exports.getNearestCity = nearCity;