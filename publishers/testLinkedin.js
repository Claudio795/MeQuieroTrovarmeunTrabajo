const puppeteer = require('puppeteer');

(async () => {
    // lancia il browser e apre una nuova pagina
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto('https://www.linkedin.com/jobs', { waitUntil: 'load'});

    // const jobLocationForm = await page.$$eval('input', inputs => {
    //     console.log(inputs.length)
    // });

    // inseriamo il tipo di qualifica o azienda:
    await page.type('.dismissable-input__input','');
    await page.keyboard.press('Tab');
    // inseriamo la zona:
    await page.type('.dismissable-input__input', 'Catania')
    await page.keyboard.press('Enter');

    // aspettiamo la risposta e printiamo la nuova URL
    await page.waitForNavigation();
    console.log('New Page URL: ', page.url())

    // TODO: inserire elaborazione delle row per restituire al publisher i lavori

    // END
    await browser.close();
})();