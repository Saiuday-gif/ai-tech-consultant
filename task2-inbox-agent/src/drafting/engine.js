const { queryKnowledgeBrain } = require("../knowledge-client/client");

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

async function processEmail(email) {
  const classification = classifyEmail(email.subject, email.body);
  const kbResponse = await queryKnowledgeBrain(email.body);

  let draftReply = "";
  if (classification.category === "Refund or cancellation") {
    draftReply = `Dear Customer,\n\nWe have received your billing/cancellation request regarding "${email.subject}". Due to account security and financial authorization protocols, a senior account manager will review your request within 24 hours.\n\nBest regards,\nCustomer Support Team`;
  } else if (classification.category === "Complaint") {
    draftReply = `Dear Customer,\n\nWe sincerely apologize for the inconvenience described. Your concern has been marked with high priority and escalated directly to our engineering leadership for investigation.\n\nBest regards,\nCustomer Operations`;
  } else if (classification.category === "Project request" || classification.category === "Quote request") {
    draftReply = `Hello,\n\nThank you for reaching out about this project requirement. Our technical consulting team will review your specifications and schedule a discovery call to provide an accurate estimate.\n\nBest regards,\nSolutions Team`;
  } else if (kbResponse.status === "answered") {
    draftReply = `Hello,\n\nRegarding your inquiry: ${kbResponse.answer}\n\nFor additional reference, please check the official documentation: ${kbResponse.sources[0]?.url || "Admin Help Center"}\n\nBest regards,\nSupport Team`;
  } else {
    draftReply = `Hello,\n\nThank you for contacting us. We have received your query and routed it to our product specialists for verification.\n\nBest regards,\nSupport Team`;
  }

  return {
    email_id: email.id,
    original_subject: email.subject,
    predicted_category: classification.category,
    risk_level: classification.risk,
    draft_reply: draftReply,
    sources: kbResponse.sources || [],
    confidence: kbResponse.confidence,
    requires_human_approval: classification.requires_human || kbResponse.needs_human
  };
}

module.exports = { classifyEmail, processEmail };