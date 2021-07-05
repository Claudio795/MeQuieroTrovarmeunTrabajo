const puppeteer = require('../node_modules/puppeteer');

const getJobLinks = async (qualification, zone) => {
    // lancia il browser e apre una nuova pagina
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto('https://www.linkedin.com/jobs', { waitUntil: 'load' });

    // const jobLocationForm = await page.$$eval('input', inputs => {
    //     console.log(inputs.length)
    // });

    // inseriamo il tipo di qualifica o azienda:
    await page.type('.dismissable-input__input', `${qualification}`);
    await page.keyboard.press('Tab');
    // inseriamo la zona:
    await page.type('.dismissable-input__input', `${zone}`)
    await page.keyboard.press('Enter');

    // aspettiamo la risposta e printiamo la nuova URL
    await page.waitForNavigation();
    console.log('New Page URL: ', page.url())

    // TODO: inserire elaborazione delle row per restituire al publisher i lavori
    let jobs = await page.$$(`[data-tracking-control-name=public_jobs_jserp-result_search-card]`);
    let jobsHandles = await Promise.all(
        jobs.map(divHandler => divHandler.getProperty('href'))
    )

    // i primi 14 link
    let links = await Promise.all(
        jobsHandles.map(handle => handle.jsonValue())
    )

    // attendiamo la chiusura del browser
    await browser.close();

    // returniamo i link
    let stringLinks = [];
    links.forEach(link => {
        stringLinks.push(link.toString());
    });
    return stringLinks;
}

exports.getJobLinks = getJobLinks;