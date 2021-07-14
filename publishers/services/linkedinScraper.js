const puppeteer = require('../node_modules/puppeteer');

const getJobLinks = async (qualification, zone) => {
    try {
        // lancia il browser e apre una nuova pagina
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        await page.goto('https://www.linkedin.com/jobs', { waitUntil: 'load' });

        // ripuliamo il default value di location:
        await page.click('.dismissable-input__button--show')

        // inseriamo il tipo di qualifica o azienda:
        await page.type('[placeholder="Cerca qualifiche o aziende"]', qualification)
        // inseriamo la zona:
        await page.type('[placeholder="Località"]', zone)
        await page.keyboard.press('Enter');

        // aspettiamo la risposta e printiamo la nuova URL
        await page.waitForNavigation();
        console.log('New Page URL: ', page.url())

        let newUrl = await page.url()

        await page.goto(newUrl, { waitUntil: 'load' })

        // TODO: inserire elaborazione delle row per restituire al publisher i lavori
        let jobs = await page.$$(`[data-tracking-control-name="public_jobs_jserp-result_search-card"]`);
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
        console.log(stringLinks)
        return stringLinks;

    } catch (error) {
        throw error;
    }
}

exports.getJobLinks = getJobLinks;