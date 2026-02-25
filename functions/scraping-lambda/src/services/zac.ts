import { calcBreakTime, trunc15Minutes, formatTime } from "../lib/time.ts";
import { publishZacRegisterEvent } from "../lib/sns.ts";

export class ZacClient {
    constructor(
        private readonly tenantId: string,
        private readonly loginId: string,
        private readonly password: string,
    ) {}
    async zacRegisterEvent (workingTime: number) {

        const breakTime = calcBreakTime(workingTime);
        const workEndTime = trunc15Minutes(workingTime + 8.5 - breakTime);

        const { hour: workHour, minute: workMinute } = formatTime(workingTime - breakTime);
        const { hour: workEndTimeHour, minute: workEndTimeMinute } = formatTime(workEndTime);
        const { hour: breakHour, minute: breakMinute } = formatTime(breakTime);

        await publishZacRegisterEvent({
            tenantId: this.tenantId,
            loginId: this.loginId,
            password: this.password,
            registerDate: new Date().toISOString(),
            workInput: {
            workStartTime: {
                hour: 9,
                minute: '30',
            },
            workEndTime: {
                hour: workEndTimeHour,
                minute: workEndTimeMinute,
            },
            breakTime: {
                hour: breakHour,
                minute: breakMinute,
            },
            workDetails: [{
                code: '53',
                workTime: {
                hour: workHour,
                minute: workMinute,
                },
                text: 'Worked project tasks.',
            }],
            },
        })
    }
}
