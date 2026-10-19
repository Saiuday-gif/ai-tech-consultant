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

module.exports = { AutonomyTracker };