---
framework_version: 1.0.0
---

# Interview Preparation Guide

<!-- SETUP: STAR examples are personalized by running /setup based on your actual experience -->

## STAR Format

Structure answers as: **Situation** (context), **Task** (your responsibility), **Action** (what you did), **Result** (outcome).

Keep answers to 1-2 minutes. Be specific. End with what you learned or would do differently.

## Ready-Made STAR Examples

### 1. Scaling Sports Statistics Pipeline Across 9 Sports (System Design & Schema Reliability)
**S:** AlonzoAI ingested real-time statistics feeds for three initial sports, but expanding to six additional sports caused mapping gaps, duplicate row accumulation, and schema drift across downstream aggregation tables.
**T:** I needed to extend the asynchronous pipeline end-to-end, prevent duplicate record buildup, and establish a repeatable configuration pattern so new sports could be added safely without manual database patches.
**A:** Built partitioned configuration packages validated by automated contract tests in pytest; implemented replace-on-load semantics for all event-level derivations; standardized upstream stat mappings; and wrote backfill and audit scripts to reconcile historical source data into Parquet analytical tables.
**R:** Successfully expanded the production platform from 3 to 9 sports with zero schema drift, eradicated silent duplicate records, and enabled fast downstream analytical queries via Parquet exports.
**Use for:** "Tell me about a time you scaled a data pipeline", "How do you handle schema evolution and data consistency?"

### 2. Bulk Data Ingestion Portal with Entity Resolution (Data Quality & Architecture)
**S:** AlonzoAI needed to ingest bulk XML and roster/schedule CSV files from diverse sports leagues and schools, but upstream data had frequent formatting anomalies, duplicate player/team names, and failed jobs that corrupted existing staging state.
**T:** As the primary contributor, I had to architect a resilient ingestion service with robust staging, fuzzy entity deduplication, and safe rollbacks.
**A:** Built a FastAPI + Celery + Redis ingestion service with job-scoped staging tables and an atomic merge mechanism so failed jobs remained fully recoverable; engineered a canonical identifier registry with tuned fuzzy roster matching; added pre-load data quality gates, an admin console for manual conflict resolution, and comprehensive pytest suites.
**R:** Eliminated duplicate player/team records across multiple seasons, provided non-blocking alerting for data anomalies, and guaranteed that bulk uploads never left dirty data in production tables.
**Use for:** "Describe a complex data problem you solved", "How do you approach entity resolution and data cleaning?", "Tell me about a time you designed an end-to-end system."

### 3. Traceability and Quality Gating in Analytics Backend (DuckDB & Performance)
**S:** The analytics backend (DuckDB on AWS Lambda) generated streak, trend, and ranking insights for editorial content, but hallucinated or untraceable metrics occasionally surfaced due to non-deterministic SQL generation.
**T:** Ensure 100% mathematical traceability for every generated statistic and reduce latency for complex aggregation queries.
**A:** Mandated query-level traceability for every generated analytical item, benchmarked outputs against a curated gold dataset, added deterministic pre-LLM filter gates, and optimized SQL aggregations within DuckDB on AWS Lambda.
**R:** Eliminated false-positive claims from editorial content, guaranteed verifiable source queries for all metrics, and maintained sub-second serverless execution.
**Use for:** "How do you ensure data accuracy in AI/analytics platforms?", "Tell me about an optimization you implemented."

### 4. Real-Time Meeting Poll Generation at IIT Ropar (Frontend & LLM Integration)
**S:** During the NPTEL Summer Internship, the team needed an interactive frontend for an automated system that transcribed live meeting audio and generated contextual audience polls in real time.
**T:** Build a responsive, low-latency UI in React and Tailwind CSS that could display dynamic poll options and live voting feedback seamlessly.
**A:** Developed dynamic polling interfaces with responsive UI components, integrated websocket/API feeds to receive LLM-generated questions, and handled state transitions cleanly under real-time streaming constraints.
**R:** Delivered a production-ready interface that successfully demonstrated automated poll generation and real-time interaction during live sessions.
**Use for:** "Tell me about a time you worked with full-stack / frontend interfaces", "How do you collaborate across teams?"

## STAR Candidates (Complete Manually)

<!-- Added by /setup Path A from resume_2026-09.tex and the portfolio (Sep 2026). Fill in S/T/A/R before using any of these in an interview. -->

### LLM claim-verification stage with a CI accuracy gate
**Source:** Resume (Sep 2026) / portfolio - AlonzoAI
**What happened:** Built the stage that splits each generated statement into checkable claims, resolves the entities, generates SQL against DuckDB to test them and judges the result; benchmarked it on a human-labelled gold dataset and wired the accuracy run in as a CI gate.
**Why it matters:** "How do you make LLM output trustworthy?", "How do you test something non-deterministic?", "Describe a quality gate you built."
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### Fixing a duplication defect in the digitised-records feed bridge
**Source:** Resume (initial) / portfolio - AlonzoAI
**What happened:** Built the lookup and source-resolution layer between two upstream feeds, found and fixed a duplication defect in that join, and added an automatic re-trigger for runs a cleanup step had halted.
**Why it matters:** "Tell me about a bug you tracked down", "How do you debug data-quality issues in production?"
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### Line Review Workflow Platform (event-driven design with Kafka)
**Source:** Portfolio - personal project
**What happened:** Designed an event-driven review workflow end to end: transactional outbox relayed to Kafka, CQRS read side, Keycloak-backed role checks, hexagonal layers enforced in CI, 19 decision records.
**Why it matters:** "Walk me through a system you designed", "Do you have Kafka / streaming experience?" (honest answer: personal project, not production), "How do you make and record architecture decisions?"
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### Cutting model calls with deterministic pre-filtering (job-posting pipeline)
**Source:** Portfolio - personal project
**What happened:** Filtered ~99% of a 7,000-posting run with deterministic rules before any model call, behind a scoring harness with an output contract, repair retries, self-consistency sampling and a content-addressed cache.
**Why it matters:** "How do you control LLM cost and reliability?", "Tell me about something you built on your own time."
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### Team Lead, Alonzo Spark Internship
**Source:** Resume (Sep 2026) / portfolio - AlonzoAI
**What happened:** Led a team during the Alonzo Spark Internship (scope, team size and dates not yet recorded).
**Why it matters:** "Tell me about a time you led a team", "How do you handle disagreement or an underperforming teammate?"
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

## Common Tough Questions

### "Why did you leave [previous company]?"
> "At AlonzoAI, I had a fantastic hands-on experience building and operating core data pipelines across nine sports from scratch. Now that those pipelines and ingestion portals are mature and in production, I am excited to take on new challenges—scaling data infrastructure, working on high-throughput distributed systems, and contributing to a larger engineering team."

### "You don't have [specific skill/experience, e.g. Kafka or Snowflake]."
> "While my recent production work has focused on high-throughput asynchronous batch pipelines using Celery, RabbitMQ, PostgreSQL, DuckDB, and AWS, the core distributed systems principles—idempotency, partitioned processing, and data consistency—are identical. I pick up new tools very quickly and have already worked with similar concepts."

### "Where do you see yourself in 5 years?"
> "I see myself as a Senior Data / Platform Engineer, leading the design of mission-critical data systems, setting data quality standards, and mentoring junior engineers in building reliable, fault-tolerant pipelines."

### "What's your biggest weakness?"
> "Because I care deeply about data correctness and preventing edge-case bugs, I sometimes spend extra time perfecting automated validation and edge-case handling early in a feature. I've learned to balance this by agreeing on clear data contracts and MVP scopes upfront so velocity stays high without sacrificing quality."

### "Why this company specifically?"
> Customize per company. Must reference: specific projects, company values, market position, or team structure. Never give a generic answer.

## Questions You Should Ask Interviewers

### About the Role
- "What does a typical week look like in this role?"
- "What would success look like in the first 6 months?"
- "What's the biggest challenge the team is facing right now?"

### About the Team
- "How big is the team, and how do you divide work?"
- "What does the development/project lifecycle look like, from idea to production?"
- "How do you onboard new team members?"

### About Tech & Growth
- "What's your current tech stack for [relevant area]?"
- "Is there room to grow into more architectural or strategic decisions?"
- "How does the team stay current with new tools and methods?"

### About Culture (use these to prevent disappointment)
- "How would you describe the team culture?"
- "What does professional development look like here?"
- "Is there flexibility for remote/hybrid work?"
- "What's the balance between development/new projects and maintenance work?"
- "How would you describe the leadership style in this team?"
- "What do people who thrive here have in common?"

## Phone/Video Interview Tips
- Have STAR examples written out (use this file)
- Keep a glass of water nearby
- Smile when speaking (it changes your tone)
- Ask for clarification if a question is vague
- It's OK to take 5 seconds to think before answering
- End with: "Is there anything else you'd like to know about my background?"

## After the Application (Best Practice)

### Follow-Up Etiquette
- **Don't call to "stand out"** or to learn more about the role post-submission - this risks a negative impression
- If the employer specified a timeline, respect it and wait
- If no timeline was given and significant time has passed (2+ weeks), a brief call to ask about status is acceptable
- If you have genuinely new, relevant information to share, a short follow-up is fine

### Thank-You Notes
- When you receive any update (interview invitation, rejection, or status update), send a brief thank-you message
- Express appreciation for their time and the process
- Keep it short (2-3 sentences)

## Roleplay Guidelines
When the user asks for interview practice:
1. Ask which role/company to simulate
2. Start with easy warm-up questions ("Tell me about yourself")
3. Progress to role-specific technical questions
4. Include 1-2 behavioral questions using the competencies from the job posting
5. End with a tough question or curveball
6. After each answer, give brief feedback: what worked, what to sharpen
7. Suggest which STAR example would work best for each question
