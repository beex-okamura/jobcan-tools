import { getSecretsValues } from '../lib/asm.ts';

export const sendSlackNotification = async (message: string) => {
  const { JOBCAN_TOOL_API_ENDPOINT, SLACK_VERIFICATION_TOKEN } = await getSecretsValues();
  await fetch(`${JOBCAN_TOOL_API_ENDPOINT}/slack/message`, {
    body: JSON.stringify({
      token: SLACK_VERIFICATION_TOKEN,
    })
  })
}
