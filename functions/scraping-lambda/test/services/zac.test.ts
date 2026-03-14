const jestObj = import.meta.jest as any;

const mockSendZacRegisterEvent = jestObj.fn();
jestObj.unstable_mockModule("../../src/lib/sqs.ts", () => ({
    sendZacRegisterEvent: mockSendZacRegisterEvent,
}));

const { ZacClient } = await import("../../src/services/zac.ts");

describe('ZacClient.zacRegisterEvent', () => {
    beforeEach(() => {
        mockSendZacRegisterEvent.mockClear();
    });

    test('workingTime=7.91の場合、workTime=7:45, workEndTime=18:15, breakTime=1:00', async () => {
        const client = new ZacClient('tenant', 'login', 'pass');
        await client.zacRegisterEvent(7.91);

        expect(mockSendZacRegisterEvent).toHaveBeenCalledWith(
            expect.objectContaining({
                workInput: expect.objectContaining({
                    workStartTime: { hour: 9, minute: '30' },
                    workEndTime: { hour: 18, minute: '15' },
                    breakTime: { hour: 1, minute: '0' },
                    workDetails: [expect.objectContaining({
                        workTime: { hour: 7, minute: '45' },
                    })],
                }),
            }),
        );
    });

    test('workingTime=6.5の場合、breakTime=0:30', async () => {
        const client = new ZacClient('tenant', 'login', 'pass');
        await client.zacRegisterEvent(6.5);

        expect(mockSendZacRegisterEvent).toHaveBeenCalledWith(
            expect.objectContaining({
                workInput: expect.objectContaining({
                    workStartTime: { hour: 9, minute: '30' },
                    workEndTime: { hour: 16, minute: '30' },
                    breakTime: { hour: 0, minute: '30' },
                    workDetails: [expect.objectContaining({
                        workTime: { hour: 6, minute: '30' },
                    })],
                }),
            }),
        );
    });

    test('workingTime=5.0の場合、breakTime=0:00', async () => {
        const client = new ZacClient('tenant', 'login', 'pass');
        await client.zacRegisterEvent(5.0);

        expect(mockSendZacRegisterEvent).toHaveBeenCalledWith(
            expect.objectContaining({
                workInput: expect.objectContaining({
                    workStartTime: { hour: 9, minute: '30' },
                    workEndTime: { hour: 14, minute: '30' },
                    breakTime: { hour: 0, minute: '0' },
                    workDetails: [expect.objectContaining({
                        workTime: { hour: 5, minute: '0' },
                    })],
                }),
            }),
        );
    });
});
