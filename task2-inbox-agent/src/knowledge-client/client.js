const TASK1_API_URL = "http://127.0.0.1:8000/query";

async function queryKnowledgeBrain(question) {
  try {
    const response = await fetch(TASK1_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    
    if (!response.ok) {
      throw new Error(`Task 1 responded with status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    return {
      answer: "Knowledge Brain service currently unreachable.",
      status: "insufficient_evidence",
      sources: [],
      confidence: 0.0,
      needs_human: true
    };
  }
}

module.exports = { queryKnowledgeBrain };