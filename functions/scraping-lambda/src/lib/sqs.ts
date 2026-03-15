import { z } from 'zod';
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';
import { SqsEventSchema } from '../entities/zac.ts';

export const sendZacRegisterEvent = async (event: z.infer<typeof SqsEventSchema>) => {
  const sqs = new SQSClient({});

  await sqs.send(
    new SendMessageCommand({
      QueueUrl: process.env.ZAC_REGISTER_EVENT_QUEUE_URL,
      MessageBody: JSON.stringify(event),
      MessageGroupId: 'zac-register',
    }),
  );
};
