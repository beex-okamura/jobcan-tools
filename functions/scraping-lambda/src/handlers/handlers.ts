import {type SQSEvent} from 'aws-lambda';
import logger from '../lib/logger.ts';
import {getBrowser} from '../lib/browser.ts';

import {JobCanClient} from '../playwright/jobcan.ts';
import {type Browser} from 'playwright';
import {type UserInfo} from '../entities/user.ts';
import { decryptPassword } from '../lib/kms.ts';
import { sendSlackNotification } from '../slack/notification.ts';

const dryRun = process.env.DRY_RUN === 'true';

export const handler = async (event: SQSEvent) => {
	const messages = event.Records.map(e => JSON.parse(e.body) as UserInfo);

	logger.info('start jobcan scraping');

	const browser = await getBrowser();

	try {
		for (const message of messages) {
			const {jobcan_user_id: userId, jobcan_password: password} = message;

			await sendSlackNotification('JOBCAN 勤怠連携処理を開始します')

			// eslint-disable-next-line no-await-in-loop
			await workPunch(browser, userId, password);

			await sendSlackNotification('JOBCAN 勤怠連携処理を終了します')
		}
	} finally {
		await browser.close();
	}

	logger.info('end jobcan scraping');
};

export const workPunch = async (browser: Browser, userId: string, password: string) => {
	

	const page = await browser.newPage();

	const plaintext = await decryptPassword(password)

	const jobcan = new JobCanClient(page);
	await jobcan.login(userId, plaintext.toString());

	if (dryRun) return;
	const res = await jobcan.workPunch();
	logger.info(res);
};
