import {type Page} from 'playwright';
import {format} from 'date-fns';
import logger from '../lib/logger.ts';
import path from 'path';
import {getEnvironments} from '../lib/environments.ts';
import { addPrefixToS3Path, uploadToS3 } from '../lib/s3.ts';
import { JobCanPunchResponse } from '../entities/jobcan.ts';

const nowDate = new Date();
const {uploadBucket,downloadDir} = getEnvironments();

export class JobCanClient {
	constructor(private readonly page: Page) { }

	async login(userId: string, password: string) {
		await this.page.goto('https://id.jobcan.jp/users/sign_in');
		await this.page.fill('#user_email', userId);
		await this.page.fill('#user_password', password);
		await this.page.click('input[type="submit"]');

		try {
			const errorMessage = await this.page.innerText('p.flash.flash__notice', {
				timeout: 1000,
			});
			if (errorMessage) {
				throw new Error(errorMessage);
			}	
		} catch (e) {
			logger.info('error message not found. login success.')
		}

		await this.page.waitForURL('https://id.jobcan.jp/account/profile')
		logger.info('login success');
	}

	async workPunch(): Promise<JobCanPunchResponse> {
		logger.info('start work punch');
		await this.page.goto('https://ssl.jobcan.jp/jbcoauth/login');

		await this.page.click('#adit-button-push');

		const response = await this.page.waitForResponse(resp => resp.url()
			.includes('https://ssl.jobcan.jp/employee/index/adit') && resp.status() === 200);

		logger.info('end work punch');

		return response.json();
	}

	async saveSnapshotAndThrowError(err: Error) {
		logger.error(err.stack);
		const snapshotName = `${format(nowDate, 'yyyyMMdd_hhmmss')}.png`;
		const body = await this.page.screenshot({
			path: path.join(downloadDir, snapshotName),
			type: 'png',
		});
		if (uploadBucket !== undefined) {
			await uploadToS3(uploadBucket, addPrefixToS3Path('Snapshot', snapshotName), body);
		}

		throw err;
	}
}
