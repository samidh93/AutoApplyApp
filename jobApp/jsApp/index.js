const puppeteer = require('puppeteer');

async function scrapeJobDetails(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);
  
  const jobDetailsSpan = await page.$('#job-details span');
  const jobDetailsText = await page.evaluate((span) => span.innerText, jobDetailsSpan);

  await browser.close();
  return jobDetailsText;
}

// Accept a URL argument from the command line
const url = "https://www.linkedin.com/jobs/view/responsable-ou-charg%C3%A9-e-de-formation-h-f-at-capgemini-engineering-3552172915/?trackingId=32aLLpS20kovjLSLATp5%2BQ%3D%3D&refId=fK0kJT2d5pKIvgc%2FsVpW1Q%3D%3D&pageNum=0&position=1&trk=public_jobs_jserp-result_search-card&originalSubdomain=fr" //process.argv[2];
scrapeJobDetails(url).then((result) => console.log(result));
