const assert = require("assert");

function classifyEmail(subject, body) {
  const content = `${subject} ${body}`.toLowerCase();
  
  if (content.includes("refund") || content.includes("cancel") || content.includes("charge")) {
    return { category: "Refund or cancellation", risk: "Critical", requires_human: true };
  }
  if (content.includes("down") || content.includes("error") || content.includes("broken") || content.includes("fails")) {
    return { category: "Troubleshooting", risk: "Moderate", requires_human: false };
  }
  if (content.includes("complaint") || content.includes("unresponsive") || content.includes("dispute") || content.includes("spam")) {
    return { category: "Complaint", risk: "Critical", requires_human: true };
  }
  if (content.includes("quote") || content.includes("pricing") || content.includes("cost") || content.includes("rate")) {
    return { category: "Quote request", risk: "High", requires_human: true };
  }
  if (content.includes("build") || content.includes("develop") || content.includes("integration") || content.includes("custom theme")) {
    return { category: "Project request", risk: "High", requires_human: true };
  }
  if (content.includes("status") || content.includes("following up") || content.includes("checking in") || content.includes("reaching out")) {
    return { category: "Follow-up", risk: "Low", requires_human: false };
  }
  return { category: "How-to", risk: "Low", requires_human: false };
}

class AutonomyTracker {
  constructor() {
    this.consecutiveApprovals = {};
    this.autonomousCategories = new Set();
    this.history = [];
  }

  recordDecision(category, wasEdited, isRejected) {
    if (!this.consecutiveApprovals[category]) {
      this.consecutiveApprovals[category] = 0;
    }

    const isHighRisk = ["Refund or cancellation", "Complaint", "Quote request"].includes(category);

    if (wasEdited || isRejected) {
      this.consecutiveApprovals[category] = 0;
      this.autonomousCategories.delete(category);
    } else {
      this.consecutiveApprovals[category] += 1;
      if (this.consecutiveApprovals[category] >= 20 && !isHighRisk) {
        this.autonomousCategories.add(category);
      }
    }

    const logEntry = {
      timestamp: new Date().toISOString(),
      category,
      wasEdited,
      isRejected,
      consecutiveCount: this.consecutiveApprovals[category],
      isAutonomousEligible: this.autonomousCategories.has(category)
    };
    this.history.push(logEntry);
    return logEntry;
  }

  isEligibleForAutonomy(category) {
    return this.autonomousCategories.has(category);
  }

  getStats() {
    return {
      counters: this.consecutiveApprovals,
      autonomousEnabled: Array.from(this.autonomousCategories),
      totalProcessed: this.history.length
    };
  }
}

function testEmailClassification() {
  const howTo = classifyEmail("How to change logo", "Where can I upload my logo?");
  assert.strictEqual(howTo.category, "How-to");
  assert.strictEqual(howTo.risk, "Low");
  assert.strictEqual(howTo.requires_human, false);

  const refund = classifyEmail("Cancel my subscription", "Please cancel and refund my charge");
  assert.strictEqual(refund.category, "Refund or cancellation");
  assert.strictEqual(refund.risk, "Critical");
  assert.strictEqual(refund.requires_human, true);

  const trouble = classifyEmail("Site is broken", "Checkout payment fails with error");
  assert.strictEqual(trouble.category, "Troubleshooting");
  assert.strictEqual(trouble.risk, "Moderate");
}

function testAutonomyCounterResetOnEdit() {
  const tracker = new AutonomyTracker();
  
  tracker.recordDecision("How-to", false, false);
  tracker.recordDecision("How-to", false, false);
  assert.strictEqual(tracker.consecutiveApprovals["How-to"], 2);

  tracker.recordDecision("How-to", true, false);
  assert.strictEqual(tracker.consecutiveApprovals["How-to"], 0);
  assert.strictEqual(tracker.isEligibleForAutonomy("How-to"), false);
}

function testAutonomyEligibilityAfterTwentyApprovals() {
  const tracker = new AutonomyTracker();

  for (let i = 0; i < 20; i++) {
    tracker.recordDecision("How-to", false, false);
  }

  assert.strictEqual(tracker.consecutiveApprovals["How-to"], 20);
  assert.strictEqual(tracker.isEligibleForAutonomy("How-to"), true);

  for (let j = 0; j < 25; j++) {
    tracker.recordDecision("Refund or cancellation", false, false);
  }
  assert.strictEqual(tracker.isEligibleForAutonomy("Refund or cancellation"), false);
}

function runAllTests() {
  try {
    testEmailClassification();
    testAutonomyCounterResetOnEdit();
    testAutonomyEligibilityAfterTwentyApprovals();
    console.log("All Task 2 unit tests passed successfully (3/3 test suites).");
  } catch (error) {
    console.error("Test failed:", error.message);
    process.exit(1);
  }
}

runAllTests();