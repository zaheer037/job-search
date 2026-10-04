---
framework_version: 1.1.1
---

# Candidate Profile

<!-- SETUP: This file is populated by running /setup -->
<!-- After running /setup, all sections will be filled with your actual information -->

## Identity
- **Name:** Zaheer Maseed
- **Location:** Hyderabad, Telangana, India (Open to Remote, Bengaluru, Pan-India)
- **Phone:** +91-6301052247
- **Email:** jaheermaseed@gmail.com
- **LinkedIn:** https://linkedin.com/in/zaheer-maseed
- **GitHub:** https://github.com/zaheer037
- **Status:** Junior Data Engineer at AlonzoAI (Immediate joiner)
- **Experience:** under 1 year full-time (Junior Data Engineer since Jan 2026) plus two summer 2025 internships - target roles asking 0-2 years
- **Constraints:** Open to Remote roles, or Hybrid/On-site in Hyderabad, Bengaluru, Andhra Pradesh, and major tech hubs in India.

### Languages
<!-- Every language you can work in professionally, with your honest level. Used by the
Language Gate in 04-job-evaluation.md and by job-scraper/search-queries.md's query-language
generation. Omit any language you don't actually work in - an undeclared language is treated as
a hard no, not a gap to smooth over. -->

| Language | Level | Notes |
|----------|-------|-------|
| English | Professional | Full professional working proficiency (written & verbal) |
| Telugu | Native | Mother tongue |
| Hindi | Conversational | Working conversational proficiency |

## Education

| Degree | Period | Institution | Key Topics |
|--------|--------|-------------|------------|
| B.E. in Computer Science and Engineering (AI) | Aug 2022 - June 2026 | Chalapathi Institute of Engineering and Technology | CGPA: 9.2/10. Machine Learning, Artificial Intelligence, Database Management Systems, Data Structures & Algorithms, Distributed Systems |

## Professional Experience

### Junior Data Engineer - AlonzoAI (Jan 2026 - Present)
Hyderabad, India (office/hybrid)
- **Sports Statistics Pipeline:** Extended asynchronous pipeline (Python, FastAPI, Celery, PostgreSQL, S3, DuckDB) ingesting third-party statistics API into object storage, loading raw JSON into PostgreSQL, and deriving game, season, and career aggregates; led rollout to six additional sports via partitioned configuration packages validated by automated contract tests.
- **Event-Level Derivation & Config:** Implemented event-level derivation and match-action configuration across all nine sports, added replace-on-load semantics to prevent duplicate accumulation, and standardized upstream stat mappings to eliminate schema drift during aggregation.
- **Backfill & Audit Tooling:** Wrote backfill and audit tooling repairing historical source and attribution data across interim tables, reconciled cross-sport metadata to surface silent mapping gaps, and exported analytical tables to Parquet for downstream consumption.
- **Bulk Data Ingestion Portal (Primary Contributor):** Built FastAPI + Celery + Redis service parsing bulk XML and roster/schedule CSV uploads into job-scoped staging tables, promoted to production by an atomic merge that keeps partially failed jobs recoverable.
- **Entity Resolution Layer:** Designed canonical identifier registry, tuned fuzzy roster matching with tiered fallback, and standardized player/team attributes to eliminate duplicate identities across seasons and feeds.
- **Data Quality & Admin Operations:** Added pre-load data-quality gates, historical/post-season handling, manual-review and conflict-resolution workflows, an admin console for targeted deletion and job re-trigger, non-blocking alerting, and pytest test coverage for aggregation/unpivot logic.
- **Analytics & Content Generation Platform:** Contributed to a serverless analytics backend (DuckDB on AWS Lambda, FastAPI, React) computing streak, ranking, and trend aggregates from templated SQL; mandated query-level traceability, benchmarked against gold datasets, and added deterministic pre-LLM filters cutting false-positive claims.
- **LLM Claim-Verification Stage:** Built the content platform's verification stage, a multi-step LLM pipeline that decomposes each generated statement into checkable claims, resolves the entities, generates SQL against DuckDB to test each claim, and judges the result; benchmarked it against a human-labelled gold dataset and wired the accuracy run in as a CI gate.
- **Semantic Retrieval & Query Layer:** Added semantic context retrieval to the review flow using open-source embedding models, added cumulative stat aggregation to the query layer, and implemented additional analytical scenarios in the generation layer.
- **Document Digitisation Pipeline:** Maintained production pipeline converting historical PDF records into structured tables via human annotation and LLM table extraction; bridged digitized records into ingestion portal with deduplicated joins and automatic job re-triggering.
- **Digitisation Operations & Feed Bridge:** Ran the pipeline institution by institution, debugging extraction, matching and consistency failures; built the lookup and source-resolution layer between two upstream feeds and fixed a duplication defect in that join; added an automatic re-trigger for runs halted by a cleanup step.
- **Operator-Facing Applications:** Built the operator apps over these pipelines: FastAPI REST endpoints with typed schemas, JWT auth with role-based access control, and multi-step upload -> validation -> approval workflows running as long-running background jobs.

### Node.js Developer Intern - Celebal Technologies (May 2025 - July 2025)
<!-- Location not stated in the resume or portfolio; confirm before putting one on a CV. Same dates as the IIT Ropar internship (held concurrently). -->
- Built a task management application on Node.js: REST endpoints for task CRUD, user authentication and persistence, verified with Postman across the request lifecycle.

### Frontend Developer Intern - Indian Institute of Technology, Ropar (May 2025 - July 2025)
Remote / Ropar, India
- Selected for the NPTEL Summer Internship Program; built React/Tailwind interfaces for an automatic poll-generation system that transcribes meetings and uses LLMs to generate contextual polls in real time.

## Independent Projects
<!-- Source: portfolio (zaheer037.github.io/portfolio), Sep 2026. Both main projects are private repos; walkthrough offered on request. -->
- **Line Review Workflow Platform** (personal, designed end to end): Event-driven workflow in which sales, accounting and billing review each lead/opportunity line, with SLA clocks, a full audit trail and field-level edit rights; either review can send a line back to Sales, and managers can escalate to a director. Every state change commits with its audit entry and an outbox event that a worker relays to Kafka; a CQRS read side builds the worklists and KPI views; role checks gate every command and product-level access rules filter every read query. Hexagonal layers enforced by import-linter in CI, pyright strict on the domain. Python 3.12, FastAPI, SQLAlchemy, PostgreSQL 16, Kafka, Keycloak, React 18, TypeScript, Docker; 13 containers, 19 decision records.
- **Job-Posting Pipeline** (personal, designed end to end): Finds companies hiring in India through the Common Crawl index, pulls postings from their ATS boards, dedupes them and ranks each one against a resume. ~99% of a 7,000-posting run filtered by deterministic rules before any model call; scoring harness with an output contract, repair retries, self-consistency sampling and a content-addressed cache; tailored resumes pass a truthfulness check that flags any new employer, school or date. Python, FastAPI, httpx, LLM APIs, LaTeX.
- **Earlier builds:** Ahaa Kitchen (order and menu management for a working restaurant, MERN stack); push-to-deploy CI/CD (GitHub Actions builds a Docker image and ships a MERN app to AWS EC2 under PM2); FAANG Tech Lab website (static site with per-course landing pages for a Guntur training institute, on Azure Static Web Apps).

## Technical Skills

### Programming & ML
- **Python** (Advanced/Production): FastAPI, Celery, Pydantic, SQLAlchemy, Alembic, pytest, DuckDB, Pandas
- **SQL** (Advanced/Production): PostgreSQL, complex joins, window functions, analytical aggregations, indexing, schema design
- **TypeScript / JavaScript** (Intermediate): React, Node.js, Tailwind CSS
- **Shell Scripting** (Proficient): Bash, Linux automation, cron, systemd

### Data Engineering & Infrastructure
- **ETL / ELT Architecture:** Batch ingestion, distributed task queues, incremental & idempotent loads, change detection, backfills, schema migrations, entity resolution & fuzzy matching
- **Databases & Storage:** PostgreSQL, DuckDB, MongoDB, Redis, Parquet, AWS S3
- **Cloud & DevOps:** AWS (Lambda, S3, EC2, CDK), Docker, Docker Compose, RabbitMQ, Git, GitHub Actions, Linux
- **Backend & APIs:** FastAPI, REST API design, typed request/response schemas, JWT auth, role-based access control (RBAC), async/background job orchestration
- **LLM Pipelines & Evaluation (production):** Multi-step LLM verification pipelines, LLM-based table extraction, evaluation against human-labelled gold datasets, CI accuracy gates, open-source embedding models for semantic retrieval
- **Event-Driven Architecture (personal-project level, not production):** Kafka (transactional outbox relay), CQRS read models, Keycloak, hexagonal architecture

### Domain Expertise
- Sports Analytics & Statistics Pipelines (9 sports)
- Bulk Ingestion, Data Quality Gating & Reconciliation Audits
- Document Digitization & LLM-Assisted Data Extraction

## Publications
<!-- None listed -->

## Awards
- **1st Prize, App Builder Competition** - HCET (2024)
- **Team Lead, Alonzo Spark Internship** - AlonzoAI <!-- dates, team size and scope not yet recorded -->
- **AlonzoAI AI Club** - evaluates emerging AI tools and shares working practices colleagues apply day to day

## Certifications
- **HackerRank SQL (Intermediate)** (2025)
- **MongoDB Associate Developer** - MongoDB University (2025)
- **Certified Foundations Associate** - Oracle (2024)

## References
Available upon request.
