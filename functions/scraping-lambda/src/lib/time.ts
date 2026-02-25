import z from "zod";
import { ZacWorkTimeSchema } from "../entities/zac.ts";

// 時間15分丸め処理
export const trunc15Minutes = (time: number): number => {
    return Math.trunc(time * 4) / 4;
}

// 休憩時間を算出する
export const calcBreakTime = (time: number): number => {
    switch(true) {
        case time > 7.5:
            return 1;
        case time > 6:
            return 0.5;
        default:
            return 0;
    }
}

// NumberをHH:mm形式の文字列に変換する
export const formatTime = (time: number): z.infer<typeof ZacWorkTimeSchema> => {
    const hour = Math.floor(time);
    const minute = time % 1 * 60;
    switch (minute) {
        case 0:
            return {
                hour,
                minute: '0',
            };
        case 15:
            return {
                hour,
                minute: '15',
            };
        case 30:
            return {
                hour,
                minute: '30',
            };
        case 45:
            return {
                hour,
                minute: '45',
            };
        default:
            return {
                hour,
                minute: '0',
            };
    }
}
