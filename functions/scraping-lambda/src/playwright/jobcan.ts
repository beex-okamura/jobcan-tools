import { type Page } from "playwright";
import { format } from "date-fns";
import logger from "../lib/logger.ts";
import path from "path";
import { getEnvironments } from "../lib/environments.ts";
import { addPrefixToS3Path, uploadToS3 } from "../lib/s3.ts";
import { JobCanPunchResponse } from "../entities/jobcan.ts";

const nowDate = new Date();
const { uploadBucket, downloadDir } = getEnvironments();

export class JobCanClient {
  constructor(private readonly page: Page) {}

  async login(userId: string, password: string) {
    await this.page.goto("https://id.jobcan.jp/users/sign_in");
    await this.page.fill("#user_email", userId);
    await this.page.fill("#user_password", password);
    await this.page.click('input[type="submit"]');

    try {
      const errorMessage = await this.page.innerText("p.flash.flash__notice", {
        timeout: 1000,
      });
      if (errorMessage) {
        throw new Error(errorMessage);
      }
    } catch (e) {
      logger.info("error message not found. login success.");
    }

    await this.page.waitForURL("https://id.jobcan.jp/account/profile");
    logger.info("login success");
  }

  async workPunch(): Promise<JobCanPunchResponse> {
    logger.info("start work punch");
    await this.page.goto("https://ssl.jobcan.jp/jbcoauth/login");

    await this.page.click("#adit-button-push");

    const response = await this.page.waitForResponse(
      (resp) =>
        resp.url().includes("https://ssl.jobcan.jp/employee/index/adit") &&
        resp.status() === 200,
    );

    logger.info("end work punch");

    return response.json();
  }

  /**
   * 労働時間を取得する
   * @returns 労働時間
   */
  /**
   * 60進数の時間（HH:mm）を10進数に変換
   * @param time HH:mm形式の時間
   * @returns 10進数の時間（例：7.5）
   */
  private convertTimeToDecimal(time: string): number {
    const [hours, minutes] = time.split(":").map(Number);
    return Math.floor((hours + minutes / 60) * 10) / 10;
  }

  async getWorkingHours(date?: string): Promise<number> {
    try {
      const targetDate = date ? new Date(date) : new Date();
      const year = targetDate.getFullYear();
      const month = targetDate.getMonth() + 1;
      const targetDay = format(targetDate, "MM/dd");

      logger.info(
        `get working hours target: year=${year}, month=${month}, day=${targetDay}`,
      );

      await this.page.goto("https://ssl.jobcan.jp/jbcoauth/login");

      // 対象年月の勤怠ページにアクセス
      await this.page.goto(
        `https://ssl.jobcan.jp/employee/attendance?list_type=normal&search_type=month&year=${year}&month=${month}`,
      );

      // 対象日の行を特定
      const targetRow = this.page.locator(`tr:has(td:has-text("${targetDay}"))`);
      const isVisible = await targetRow.isVisible();

      if (!isVisible) {
        throw new Error(`${targetDay}の勤務データが見つかりませんでした`);
      }

      // 労働時間を取得 (7番目のtd要素)
      const workingHours = await targetRow.locator("td").nth(6).innerText();
      logger.info(`raw working hours text: "${workingHours}"`);

      if (!workingHours) {
        logger.warn(`${targetDay}の労働時間が取得できませんでした`);
        return 0;
      }

      // 60進数から10進数に変換して返却
      return this.convertTimeToDecimal(workingHours.trim());
    } catch (error) {
      await this.saveSnapshotAndThrowError(error as Error);
      throw error;
    }
  }

  async saveSnapshotAndThrowError(err: Error) {
    logger.error(err.stack);
    const snapshotName = `${format(nowDate, "yyyyMMdd_hhmmss")}.png`;
    const body = await this.page.screenshot({
      path: path.join(downloadDir, snapshotName),
      type: "png",
    });
    if (uploadBucket !== undefined) {
      await uploadToS3(
        uploadBucket,
        addPrefixToS3Path("Snapshot", snapshotName),
        body,
      );
    }

    throw err;
  }
}
