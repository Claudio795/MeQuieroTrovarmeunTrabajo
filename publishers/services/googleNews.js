let googleNewsAPI = require('../node_modules/google-news-json');

let getNews = async () => {
    let news = await googleNewsAPI.getNews(googleNewsAPI.TOP_NEWS, null, "it-IT").catch(err => console.log(err));
    let items = news.items;


    let articoli = [];
    items.forEach(item => {
        let articoloStrutturato = `${item.title}: ${item.link}`;
        articoli.push(articoloStrutturato);
    });

    // let articoliReturn = [articoli[0], articoli[1], articoli[2], articoli[3], articoli[4]]
    // console.log(articoliReturn);
    // returniamo i primi 5 articoli
    return [articoli[0], articoli[1], articoli[2], articoli[3], articoli[4]];
}

module.exports = getNews;