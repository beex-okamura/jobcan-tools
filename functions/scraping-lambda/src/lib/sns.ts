import { z } from 'zod';
import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';
import { SnsEventSchema } from '../entities/zac.ts';

export const publishZacRegisterEvent = async (event: z.infer<typeof SnsEventSchema>[]) => {
  const sns = new SNSClient({});

  await sns.send(
    new PublishCommand({
      TopicArn: process.env.ZAC_REGISTER_EVENT_TOPIC_ARN,
      Message: JSON.stringify(event),
    }),
  );
};
