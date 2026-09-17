# 05 - Test Plan: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## Test Levels & Tools
- **Data/Unit Tests:** `pytest`, `pandas.testing`
- **ML/Model Tests:** `pytest`, `scikit-learn` metrics, custom SHAP additivity checks
- **UI/Frontend Tests:** `Playwright` (for end-to-end user flows), `Lighthouse` (for web performance)
- **Monitoring/Drift:** `Evidently AI`

## Test Cases

| ID | Category | Description | Expected Result |
|----|----------|-------------|-----------------|
| TC-01 | Data | Ingest data containing PII (emails, names) | Output data frame contains only masked/hashed values; no plaintext PII remains. |
| TC-02 | Data | Handle missing categorical and numeric values | Pipeline successfully imputes numericals (median) and categoricals (mode/'Unknown'). |
| TC-03 | Model | Validate model Recall constraint | Evaluated recall on the test holdout set is strictly > 80%. |
| TC-04 | Model | Validate model Precision constraint | Evaluated precision on the test holdout set is strictly > 65%. |
| TC-05 | Model | SHAP Additivity Theorem Check | Base value + sum(SHAP values) == model output margin for a random sample of 100 rows. |
| TC-06 | ML Pipeline | Data Leakage Check | No target variables or post-churn event variables are present in the feature matrix. |
| TC-07 | System | Cost Matrix Threshold calculation | The thresholding function returns a boundary that strictly minimizes the provided FP/FN cost matrix compared to default 0.5. |
| TC-08 | System | Offline SHAP Cache execution | Batch job successfully writes 1000 records to SQLite and exits with status 0. |
| TC-09 | UI/E2E | Dashboard Load Time | Lighthouse/Playwright reports initial render and LCP < 2.0 seconds. |
| TC-10 | UI/E2E | Search valid Customer ID | Dashboard renders risk score, segment, and SHAP waterfall plot for that customer. |
| TC-11 | UI/E2E | Search invalid Customer ID | Graceful error message displayed ("Customer not found"), app does not crash. |
| TC-12 | UI/E2E | Export Batch Inference CSV | Clicking export downloads a CSV containing 'CustomerID', 'Risk_Score', and 'Action'. |
| TC-13 | UI/E2E | Submit Feedback Loop | Clicking "Action Successful" writes a timestamped record to the tracking database. |
| TC-14 | ML Ops | Concept Drift Detection | Running Evidently AI on a shifted dataset generates an alert indicating PSI > 0.2. |
| TC-15 | Performance| Concurrent Load Test | Locust simulates 50 concurrent users querying the dashboard; p95 latency remains < 3s, 0% error rate. |
