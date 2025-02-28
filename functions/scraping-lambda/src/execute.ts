import { getBrowser } from "./lib/browser.ts";
import { workPunch } from "./handlers/handlers.ts";

const { JOBCAN_SCRAPING_LAMBDA_USER, JOBCAN_SCRAPING_LAMBDA_PASSWORD } =
  process.env;

const browser = await getBrowser();

if (!JOBCAN_SCRAPING_LAMBDA_USER || !JOBCAN_SCRAPING_LAMBDA_PASSWORD) {
  throw new Error("Environment variables are not set");
}

await workPunch(
  browser,
  JOBCAN_SCRAPING_LAMBDA_USER,
  JOBCAN_SCRAPING_LAMBDA_PASSWORD,
  {
    isDecryptPassword: false,
  },
);

// await browser.close();
