// https://github.com/steffenmllr/find-nearest-cities
const nearestStations = require('find-nearest-cities')

const latitude = 37.515302;
const longitude = 15.069540;

const maxDistance = 10000;
const maxResults = 3;

// const cities = nearestStations.nearestCities(latitude, longitude);
const cities = nearestStations(latitude, longitude, maxDistance, maxResults);

//function getNearestCities() {
//    return JSON.stringify(
//        JSON.parse(nearestStations(latitude, longitude))
//    );
//}

console.log(`${JSON.stringify(cities)}`);

let city = JSON.parse(JSON.stringify(nearestStations(latitude, longitude, maxDistance, maxResults)));
console.log(`${city[0].name}`);