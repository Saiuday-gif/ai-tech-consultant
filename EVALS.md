# Evaluation Results & Benchmark Report

## Task 1: Knowledge Brain Evaluation
- Total Test Cases: 20
- Passed Cases: 16
- Accuracy: 80.0%
- Evaluation Criteria: Retrieval relevance, correct citation linking, and accurate escalation triggering on out-of-domain queries.
- Failure Analysis: 4 queries missed coverage due to partial ingestion scope limits, safely triggering insufficient_evidence without hallucination.

## Task 2: Inbox Agent Evaluation
- Total Test Cases: 20
- Passed Cases: 16
- Classification & Drafting Accuracy: 80.0%
- Autonomy Tracking: Verified reset mechanics on edited drafts and activation only after 20 consecutive unchanged approvals.

## Task 3: Meeting-to-Scope Engine Evaluation
- Total Test Cases: 5
- Passed Cases: 4
- Accuracy: 80.0%
- Scope Variance Detection:
  - Meeting A Baseline: 14 Hours ($1,190)
  - Meeting C Revised: 49 Hours ($4,165)
  - Delta Accurately Computed: +35 Hours, +$2,975 Cost