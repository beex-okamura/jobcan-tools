import {chromium} from 'playwright';
import logger from './logger.ts';

export const getBrowser = async () => {
	const headlessMode = process.env.HEADLESS_MODE === 'true';
	logger.debug(`puppeteer browser is docker? = ${String(headlessMode)}`);

	return chromium.launch(headlessMode ? {
		args: [
			'--no-sandbox',
			'--disable-setuid-sandbox',
			'--disable-dev-shm-usage',
			'--disable-gpu',
			'--no-first-run',
			'--no-zygote',
			'--single-process',
		],
	} : {
		headless: false,
	});
};
