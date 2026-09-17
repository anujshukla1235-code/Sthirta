# 03 - Sprint Plan: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## Sprint 1: Data Pipeline, Privacy, & Baseline Model
**Focus:** Secure data ingestion and initial model performance.
- **Task 1.1:** Set up repository, CI/CD linting, and environment scaffolding. (2 pts)
- **Task 1.2:** Implement data ingestion script with regex-based PII masking. (3 pts)
- **Task 1.3:** Perform EDA and feature engineering (handle missing values, encode categoricals). (3 pts)
- **Task 1.4:** Train baseline XGBoost classifier and evaluate against KPIs (Recall > 80%). (5 pts)
- **Dependencies:** Task 1.2 blocks 1.3 and 1.4.
- **Risks:** Imbalanced classes may require SMOTE or scale_pos_weight tuning to hit the 80% recall target.

## Sprint 2: Explainability & Cost-Benefit Optimization
**Focus:** SHAP integration, caching architecture, and business logic.
- **Task 2.1:** Implement Cost Matrix optimization for classification threshold. (5 pts)
- **Task 2.2:** Generate SHAP values using TreeExplainer in an offline batch job. (3 pts)
- **Task 2.3:** Build the SQLite/Parquet caching layer for SHAP values. (5 pts)
- **Task 2.4:** Develop segmentation logic based on top SHAP drivers and map to retention actions. (3 pts)
- **Dependencies:** Task 2.2 blocks 2.3 and 2.4.
- **Risks:** SHAP batch computation taking too long; will need chunking or parallel processing.

## Sprint 3: Dashboard Development & CRM Integration
**Focus:** User-facing application and operationalizing outputs.
- **Task 3.1:** Scaffold Streamlit app and implement cached data loading. (3 pts)
- **Task 3.2:** Build Customer Profile view with SHAP waterfall plots (latency < 2s). (5 pts)
- **Task 3.3:** Add batch inference CSV export functionality. (2 pts)
- **Task 3.4:** Implement feedback loop tracking UI (Success/Failure logging). (3 pts)
- **Dependencies:** Task 2.3 is required before 3.1.
- **Risks:** Streamlit rendering of large SHAP plots can be slow; optimize plotting libraries.

## Sprint 4: Drift Detection, Testing & Deployment
**Focus:** Reliability, maintenance automation, and production release.
- **Task 4.1:** Integrate Evidently AI for data/concept drift and PSI calculation. (5 pts)
- **Task 4.2:** Write automated test suites (Pytest for ML, Playwright for UI). (3 pts)
- **Task 4.3:** Deploy to Streamlit Community Cloud using `secrets.toml`. (2 pts)
- **Task 4.4:** Finalize documentation and architectural diagrams. (1 pt)
- **Dependencies:** All previous sprints must be merged and stable.
- **Risks:** Streamlit Cloud resource limits (RAM) might cause OOM errors during deployment.

## Definition of Done (DoD)
- Code is peer-reviewed (simulated) and merged into `main`.
- Automated tests pass in CI (GitHub Actions) with > 80% code coverage.
- Code passes Ruff/Flake8 linting and Black formatting.
- Acceptance criteria for the respective user story are met and verified.
- Deployment successfully reflects the latest changes without regression.
