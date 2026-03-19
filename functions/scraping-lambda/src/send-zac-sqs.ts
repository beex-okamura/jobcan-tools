import { ZacClient } from "./services/zac.ts";

const [tenantId, loginId, password, workingTimeStr] = process.argv.slice(2);

if (!tenantId || !loginId || !password || !workingTimeStr) {
  console.error(
    "Usage: npm run send-zac-sqs -- <tenantId> <loginId> <password> <workingTime>",
  );
  console.error("Example: npm run send-zac-sqs -- my-tenant user1 pass123 8.5");
  process.exit(1);
}

const workingTime = parseFloat(workingTimeStr);
if (isNaN(workingTime) || workingTime <= 0) {
  console.error("workingTime must be a positive number");
  process.exit(1);
}

console.log(`Sending ZAC register event: tenantId=${tenantId}, loginId=${loginId}, workingTime=${workingTime}`);

await new ZacClient(tenantId, loginId, password).zacRegisterEvent(workingTime);

console.log("Message sent successfully.");
