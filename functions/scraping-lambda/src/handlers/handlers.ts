import { type SQSEvent } from "aws-lambda";
import logger from "../lib/logger.ts";
import { getBrowser } from "../lib/browser.ts";

import { JobCanClient } from "../playwright/jobcan.ts";
import { type Browser } from "playwright";
import { ScrapingPayload } from "../entities/jobcan.ts";
import { decryptPassword } from "../lib/kms.ts";
import { sendSlackNotification } from "../slack/notification.ts";

const dryRun = process.env.DRY_RUN === "true";

interface Options {
  isDecryptPassword?: boolean;
}

export const handler = async (event: SQSEvent) => {
  const messages = event.Records.map(
    (e) => JSON.parse(e.body) as ScrapingPayload,
  );

  logger.info("start jobcan scraping");

  const browser = await getBrowser();

  try {
    for (const message of messages) {
      const {
        jobcan_user_id: userId,
        jobcan_password: password,
        channel,
        choice_work_type: workType,
      } = message;

      await sendSlackNotification(channel, "JOBCAN 勤怠連携処理を開始します");

      // eslint-disable-next-line no-await-in-loop
      const workingTime =
        Math.round((await workPunch(browser, userId, password)) * 100) / 100;

      if (workType === "clock_out") {
        await sendSlackNotification(
          channel,
          `本日の労働時間は${workingTime}です`,
        );
      }

      await sendSlackNotification(channel, "JOBCAN 勤怠連携処理を終了します");
    }
  } finally {
    await browser.close();
  }

  logger.info("end jobcan scraping");
};

export const workPunch = async (
  browser: Browser,
  userId: string,
  password: string,
  options?: Options,
): Promise<number> => {
  const { isDecryptPassword = true } = options || {};
  const page = await browser.newPage();

  const plaintext = isDecryptPassword
    ? (await decryptPassword(password)).toString()
    : password;

  const jobcan = new JobCanClient(page);
  await jobcan.login(userId, plaintext);

  if (dryRun) return 0;
  const res = await jobcan.workPunch();
  logger.info(res);

  const workingHours = await jobcan.getWorkingHours();
  logger.info(workingHours);
  return workingHours;
};
