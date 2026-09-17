# 07 - Maintenance & Retrospective: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## Automated Monitoring & Drift Detection
Manual checks are insufficient for ML pipelines. We implement an automated monitoring strategy:
- **Data & Concept Drift:** An automated job runs Evidently AI weekly, comparing the distribution of new incoming data against the original training dataset.
- **Metrics Tracked:** Population Stability Index (PSI) for numerical features, and Kolmogorov-Smirnov (KS-test) for target distributions.
- **Alerting:** If PSI > 0.2 on highly weighted SHAP features, an automated Slack/Email alert is triggered to the Data Engineering and ML Engineering teams.

## Retraining & Update Triggers
The XGBoost model is NOT retrained on a fixed schedule. Retraining is triggered when:
1. **Drift Alert:** The Evidently AI drift report exceeds the PSI threshold.
2. **Performance Degradation:** The feedback loop tracking UI indicates that retention success rates have dropped below 40% for two consecutive weeks.
3. **Major Business Change:** A new product tier is introduced, fundamentally altering the customer lifecycle.

## Incident Response Procedures
- **OOM (Out of Memory) Crashes:** If the Streamlit dashboard crashes due to memory limits, the ML Engineer must optimize the Pandas dataframe loads or shift the SQLite database to an external managed service (e.g., Supabase/Postgres).
- **Data Ingestion Failure:** If the pipeline ingests raw PII (failing the regex mask), the automated pipeline halts immediately, drops the corrupted tables, and pages the Data Engineer.

## Sprint Retrospective (Sprint 4 Example)

**What went well:**
- The decision to pre-compute SHAP values and cache them in SQLite was highly successful. Dashboard latency dropped from >15 seconds per request to ~800ms.
- Cost Matrix optimization provided a tangible, business-friendly metric for the VP Revenue persona.

**What was harder than expected:**
- Integrating Evidently AI into the pipeline required more boilerplate code than anticipated, particularly in formatting the baseline data for the KS-tests.
- Managing Streamlit's internal caching (`@st.cache_data`) alongside our SQLite cache led to state-management bugs early in the sprint.

**What will I change next time:**
- Introduce Playwright for frontend testing much earlier in the cycle. We caught several UI bugs late because we relied on manual acceptance testing until Sprint 4.

**Concrete actions for next cycle:**
- Implement a lightweight Airflow or Prefect orchestrator to manage the batch inference jobs, rather than relying on manual scripts.
- Migrate the local SQLite cache to a managed cloud database to support concurrent writes from the feedback loop UI.
