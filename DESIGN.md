# Technical Architecture & System Design

## 1. Knowledge Brain (Task 1)
- Crawler & Parsing: Sitemap crawler targets support documentation with manifest-driven deduplication using MD5 hashes.
- Retrieval Engine: TF-IDF Vector Space Model combined with Cosine Similarity provides reliable fallback and zero-cost retrieval.
- Multimodal Grounding: Image URLs and metadata are extracted, mapped, and linked directly to query citations.
- Escalation Protocol: Unanswered or low-confidence queries (<0.20 score) automatically flag needs_human: true and persist into an escalation review queue.

## 2. Inbox Agent (Task 2)
- Email Categorization: Classifies incoming messages across 7 business categories with assigned risk tiers.
- Grounding: Queries Task 1 API to attach factual solutions and citations to draft responses.
- Autonomy Engine: Enforces the 20-consecutive-approval rule. Edits or rejections immediately reset category counters. Critical risk categories (Refunds, Complaints) are permanently barred from full autonomy.

## 3. Meeting-to-Scope Engine (Task 3)
- Extraction Agent: Parses unstructured client-consultant dialogue into discrete technical deliverables.
- Feasibility Agent: Cross-references requirements against Task 1 knowledge endpoints to separate native capabilities from custom engineering.
- Estimator & Diff Engine: Computes hourly estimates and dynamically audits variance between initial and follow-up meeting transcripts.