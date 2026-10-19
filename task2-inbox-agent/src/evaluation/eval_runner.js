const emails = require("../email/emails_dataset.json");
const { classifyEmail, processEmail } = require("../drafting/engine");

async function runEvals() {
  console.log("Running Task 2 Evaluation Suite (20 representative test cases)...\n");
  const testSelection = emails.slice(0, 20);
  let passed = 0;

  for (let idx = 0; idx < testSelection.length; idx++) {
    const testEmail = testSelection[idx];
    const classification = classifyEmail(testEmail.subject, testEmail.body);
    const processed = await processEmail(testEmail);

    const categoryMatches = classification.category === testEmail.category;
    const draftGenerated = processed.draft_reply && processed.draft_reply.length > 30;
    const isPass = categoryMatches && draftGenerated;

    if (isPass) passed++;

    console.log(`Case IN-${String(idx + 1).padStart(3, "0")} | Expected: ${testEmail.category} | Predicted: ${classification.category} | Passed: ${isPass}`);
  }

  const accuracy = ((passed / testSelection.length) * 100).toFixed(1);
  console.log("\n==================================");
  console.log(`Total Evaluated: ${testSelection.length}`);
  console.log(`Passed: ${passed}`);
  console.log(`Classification & Drafting Accuracy: ${accuracy}%`);
  console.log("==================================");
}

runEvals();