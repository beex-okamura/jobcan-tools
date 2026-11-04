import { type SQSEvent } from "aws-lambda";
import logger from "../lib/logger.ts";
import { getBrowser } from "../lib/browser.ts";

import { JobCanClient } from "../playwright/jobcan.ts";
import { type Browser } from "playwright";
import { GetWorkingHoursPayload, ScrapingPayload } from "../entities/jobcan.ts";
import { decryptPassword } from "../lib/kms.ts";
import { sendSlackNotification } from "../slack/notification.ts";
import { ZacClient } from "../services/zac.ts";

const dryRun = process.env.DRY_RUN === "true";

interface Options {
  isDecryptPassword?: boolean;
}

export const handler = async (event: SQSEvent) => {
  logger.info("start jobcan scraping");

  const browser = await getBrowser();

  try {
    for (const record of event.Records) {
      const {
        jobcan_user_id: userId,
        jobcan_password: password,
        zac_tenant_id: tenantId,
        zac_user_id: loginId,
        zac_password: zacPassword,
        channel,
        choice_work_type: workType,
      } = JSON.parse(record.body) as ScrapingPayload;

      // 成功時の結果は zac-scraping の登録完了通知で分かるため、ここでは失敗時のみ通知する
      try {
        // eslint-disable-next-line no-await-in-loop
        const workingTime = await workPunch(browser, userId, password);

        if (workType === "clock_out") {
          // eslint-disable-next-line no-await-in-loop
          await new ZacClient(tenantId, loginId, zacPassword).zacRegisterEvent(
            workingTime,
            channel,
          );
        }
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : String(error);
        // eslint-disable-next-line no-await-in-loop
        await sendSlackNotification(
          channel,
          `:x: JOBCAN 勤怠連携でエラーが発生しました（${record.attributes.ApproximateReceiveCount}回目）\nエラー: ${errorMessage}`,
        );
        throw error;
      }
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

  if (dryRun === false) {
    const res = await jobcan.workPunch();
    logger.info(res);
  }

  const workingHours = await jobcan.getWorkingHours();
  logger.info(workingHours);
  return workingHours;
};

export const getWorkingHoursHandler = async (
  event: GetWorkingHoursPayload,
): Promise<number> => {
  const { jobcan_user_id: userId, jobcan_password: password, date } = event;

  logger.info("start get working hours");

  const browser = await getBrowser();

  try {
    const page = await browser.newPage();
    const plaintext = (await decryptPassword(password)).toString();

    const jobcan = new JobCanClient(page);
    await jobcan.login(userId, plaintext);

    const workingHours = await jobcan.getWorkingHours(date);
    logger.info(`working hours: ${workingHours}`);

    return workingHours;
  } finally {
    await browser.close();
    logger.info("end get working hours");
  }
};
