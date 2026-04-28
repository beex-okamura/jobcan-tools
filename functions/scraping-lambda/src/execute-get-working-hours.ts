import { getBrowser } from "./lib/browser.ts";
import { JobCanClient } from "./playwright/jobcan.ts";
import logger from "./lib/logger.ts";

const {
  JOBCAN_SCRAPING_LAMBDA_USER,
  JOBCAN_SCRAPING_LAMBDA_PASSWORD,
  TARGET_DATE,
} = process.env;

if (!JOBCAN_SCRAPING_LAMBDA_USER || !JOBCAN_SCRAPING_LAMBDA_PASSWORD) {
  throw new Error("Environment variables are not set");
}

const browser = await getBrowser();

try {
  const page = await browser.newPage();
  const jobcan = new JobCanClient(page);
  await jobcan.login(
    JOBCAN_SCRAPING_LAMBDA_USER,
    JOBCAN_SCRAPING_LAMBDA_PASSWORD,
  );

  const workingHours = await jobcan.getWorkingHours(TARGET_DATE);
  logger.info(`working hours: ${workingHours}`);
} finally {
  await browser.close();
}
