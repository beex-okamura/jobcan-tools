process.env.HEADLESS_MODE = 'true'

import { handler } from "../../src/handlers/handlers.ts"

describe('handlers.test', () => {
    test('should pass', async () => {
        await handler({
            Records: [
                {
                    body: JSON.stringify({
                        userId: 'userId',
                        password: 'password'
                    }),
                    messageId: 'messageId',
                    receiptHandle: 'receiptHandle',
                    attributes: {
                        ApproximateReceiveCount: 'ApproximateReceiveCount',
                        SentTimestamp: 'SentTimestamp',
                        SenderId: 'SenderId',
                        ApproximateFirstReceiveTimestamp: 'ApproximateFirstReceiveTimestamp',
                    },
                    messageAttributes: {
                        test: {
                            stringValue: 'test',
                            binaryValue: 'binaryValue',
                            stringListValues: ['stringListValues'],
                            binaryListValues: ['binaryListValues'],
                            dataType: 'dataType',
                        }
                    },
                    md5OfBody: 'md5OfBody',
                    eventSource: 'eventSource',
                    eventSourceARN: 'eventSourceARN',
                    awsRegion: 'awsRegion',
                }
            ],
        })
    }, 20000)
})
