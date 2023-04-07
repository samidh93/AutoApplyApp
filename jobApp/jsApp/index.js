const puppeteer = require('puppeteer');

async function getJobDetails(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);

  // Wait for the job details span to appear
  await page.waitForSelector('#job-details span');

  // Extract the job details text
  const jobDetailsSpan = await page.$('#job-details span');
  const jobDetailsText = await page.evaluate(jobDetailsSpan => jobDetailsSpan.innerText, jobDetailsSpan);

  await browser.close();
  return jobDetailsText;
}
async function getText(url, selector) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);
  await page.waitForSelector(selector);
  const element = await page.$(selector);
  if (element) {
    const text = await page.evaluate(element => element.innerText, element);
    return text;
  } else {
    return null;
  }
}
// Call the function with the URL as an argument
const url = "https://www.linkedin.com/jobs/view/responsable-ou-charg%C3%A9-e-de-formation-h-f-at-capgemini-engineering-3552172915/?trackingId=32aLLpS20kovjLSLATp5%2BQ%3D%3D&refId=fK0kJT2d5pKIvgc%2FsVpW1Q%3D%3D&pageNum=0&position=1&trk=public_jobs_jserp-result_search-card&originalSubdomain=fr";
jobTitle= getText(url, 'body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div > div.p5 > h1');
console.log(jobTitle);

getJobDetails(url).then(result => console.log(result));



