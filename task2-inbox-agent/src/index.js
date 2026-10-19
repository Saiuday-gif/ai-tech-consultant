const emails = require("./email/emails_dataset.json");
const { processEmail } = require("./drafting/engine");
const { AutonomyTracker } = require("./feedback/tracker");

async function main() {
  const tracker = new AutonomyTracker();
  console.log("=== AI TECH CONSULTANT: INBOX AGENT ===");
  console.log(`Loaded ${emails.length} customer emails from dataset.\n`);

  for (let i = 0; i < 5; i++) {
    const email = emails[i];
    const processed = await processEmail(email);

    console.log(`[Processing ${processed.email_id}] Category: ${processed.predicted_category} | Risk: ${processed.risk_level}`);
    console.log(`Subject: "${processed.original_subject}"`);
    console.log(`Draft Reply:\n${processed.draft_reply}`);
    console.log(`Requires Human Review: ${processed.requires_human_approval}`);

    const simulatedEdit = false;
    const decision = tracker.recordDecision(processed.predicted_category, simulatedEdit, false);
    console.log(`Autonomy Counter for '${processed.predicted_category}': ${decision.consecutiveCount}\n----------------------------------`);
  }

  console.log("Simulating 20 consecutive unchanged approvals for 'How-to' category...");
  for (let j = 0; j < 20; j++) {
    tracker.recordDecision("How-to", false, false);
  }

  console.log("Status after 20 approvals:", tracker.getStats());
}

main();