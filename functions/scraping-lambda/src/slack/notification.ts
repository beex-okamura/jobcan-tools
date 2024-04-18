import { getSecretsValues } from "../lib/asm.ts";

export const sendSlackNotification = async (
  channel: string,
  message: string,
) => {
  const { JOBCAN_TOOL_API_ENDPOINT, SLACK_VERIFICATION_TOKEN } =
    await getSecretsValues();
  await fetch(`${JOBCAN_TOOL_API_ENDPOINT}/slack/message`, {
    headers: {
      "content-type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      token: SLACK_VERIFICATION_TOKEN,
      text: message,
      channel,
    }),
  });
};
