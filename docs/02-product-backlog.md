# 02 - Product Backlog: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## User Stories

| ID | Persona | User Story | Acceptance Criteria | Priority | Story Points |
|---|---|---|---|---|---|
| US-01 | Data Engineer | As a Data Engineer, I want to automatically mask PII upon data ingestion so that customer privacy is maintained. | 1. All names and contact info hashed/masked. 2. Pipeline fails if PII regex match is detected in output. | Must | 3 |
| US-02 | ML Engineer | As an ML Engineer, I want to train an XGBoost model on historical data so that we can accurately predict churn probabilities. | 1. Recall > 80%. 2. Precision > 65%. 3. F1 Score > 72%. 4. Training logged in MLflow. | Must | 8 |
| US-03 | ML Engineer | As an ML Engineer, I want to optimize classification thresholds using a Cost Matrix (FP vs FN) so that retention ROI is maximized. | 1. Threshold optimizes cost function (FN cost = lost LTV, FP cost = discount cost). 2. Financial impact reported. | Must | 5 |
| US-04 | ML Engineer | As an ML Engineer, I want to pre-compute SHAP values offline and cache them in SQLite/Parquet so that dashboard latency is minimized. | 1. SHAP TreeExplainer runs in batch. 2. Values stored in indexed SQLite/Parquet. | Must | 5 |
| US-05 | Customer Success Manager | As a Customer Success Manager, I want an interactive Retention Dashboard so that I can view risk scores and SHAP waterfall plots for specific customers. | 1. Dashboard loads in < 2s. 2. Retrieves cached SHAP values. 3. Displays top 5 churn drivers per customer. | Must | 8 |
| US-06 | Retention Marketing Lead | As a Retention Marketing Lead, I want customers segmented by primary churn drivers so that I can apply targeted retention strategies. | 1. K-means or rule-based segmentation applied to SHAP values. 2. Segments mapped to distinct retention actions. | Must | 5 |
| US-07 | Customer Success Manager | As a Customer Success Manager, I want to export a batch inference CSV so that I can upload the targets directly into our CRM. | 1. CSV includes CustomerID, Risk Score, Segment, Recommended Action. 2. PII remains masked. | Must | 3 |
| US-08 | ML Engineer | As an ML Engineer, I want to integrate Evidently AI to calculate PSI and detect data/concept drift so that I know when to retrain the model. | 1. Drift report generated weekly. 2. Alert triggered if PSI > 0.2. | Should | 5 |
| US-09 | VP Revenue | As a VP Revenue, I want a feedback loop tracking mechanism in the dashboard so that we can record whether a retention action was successful. | 1. UI allows marking "Action Successful/Failed". 2. Results written to tracking database. | Should | 5 |
| US-10 | Data Engineer | As a Data Engineer, I want automated unit and integration tests in the CI pipeline so that broken code cannot be deployed. | 1. > 80% code coverage. 2. CI fails on test failure or lint errors. | Should | 3 |
| US-11 | Customer Success Manager | As a Customer Success Manager, I want to search for a customer by their masked ID with auto-complete so that I can quickly find their profile. | 1. Search latency < 500ms. 2. Handles typos/partial matches gracefully. | Could | 2 |
| US-12 | ML Engineer | As an ML Engineer, I want to implement load testing on the Streamlit dashboard so that we verify it can handle 50 concurrent users. | 1. Locust/Playwright tests configured. 2. p95 response time < 3s under load. | Could | 3 |
