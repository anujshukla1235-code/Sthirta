# 04 - System Design: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## High-Level Architecture

```text
+-------------------+       +-----------------------+       +------------------------+
|   Raw Data (CSV)  | ----> | PII Masking & Preproc | ----> | Feature Store (Parquet)|
+-------------------+       +-----------------------+       +------------------------+
                                                                        |
                                                                        v
+-------------------+       +-----------------------+       +------------------------+
| Cost/Benefit Opt. | <---- |   XGBoost Classifier  | <---- | Training / Scoring Job |
+-------------------+       +-----------------------+       +------------------------+
          |                             |
          v                             v
+-------------------+       +-----------------------+       +------------------------+
| Retention Actions |       | SHAP TreeExplainer    | ----> | SQLite / Parquet Cache |
+-------------------+       +-----------------------+       +------------------------+
          |                                                             |
          +-----------------------------+-------------------------------+
                                        |
                                        v
                            +-----------------------+
                            | Streamlit Dashboard   |
                            +-----------------------+
                            | - SHAP Waterfall      |
                            | - CSV Export          |
                            | - Feedback Loop UI    |
                            +-----------------------+
                                        |
                                        v
                            +-----------------------+
                            | Feedback Tracking DB  |
                            +-----------------------+
```

## Tech Stack & Justification
- **Model:** XGBoost. Chosen over Neural Networks because tree-based models natively support rapid, exact SHAP value computation via TreeExplainer, and perform exceptionally well on tabular data.
- **Explainability:** SHAP. Provides theoretically sound, consistent feature attributions.
- **Storage/Cache:** Parquet for feature storage; SQLite for fast, indexed key-value retrieval of SHAP arrays during dashboard runtime.
- **Web Layer:** Streamlit. Enables rapid prototyping of Python-based data applications.
- **Monitoring:** Evidently AI. Industry standard for detecting data drift, concept drift, and target drift.

## Data Flow & Storage Strategy
1. **Ingestion & Masking:** Raw tabular data is ingested. Regex-based masking immediately strips or hashes PII (names, emails).
2. **Offline Batch Processing:** 
   - A batch job runs inference using the XGBoost model.
   - Predictions are thresholded using the Cost Matrix optimization layer.
   - SHAP TreeExplainer computes attributions for every customer.
   - Results (Predictions, Top Features, SHAP arrays) are written to a localized SQLite database (or Parquet files) to act as a low-latency serving cache.
3. **Serving:** The Streamlit dashboard queries the SQLite cache via Customer ID. No heavy model inference or SHAP computation happens at runtime.
4. **Feedback Loop:** User interactions (e.g., "Retention Action Applied") are written back to a lightweight tracking DB (SQLite/Postgres).

## Non-Functional Requirements (NFRs)
- **Latency:** Dashboard profile load time must be < 2 seconds at the 95th percentile (p95).
- **Compute Efficiency:** Offline SHAP computation batch job must process 10,000 records in < 5 minutes.
- **Memory Footprint:** Streamlit Cloud instance must not exceed 800MB RAM usage to prevent OOM termination.
- **Security:** Zero plaintext PII present in any intermediate Parquet files or caches.

## Key Architectural Decisions
- **Decoupling Inference from Serving:** By completely separating the SHAP computation from the web app, we guarantee high responsiveness for the Customer Success persona and avoid the "spinning loader" problem inherent to synchronous ML web apps.
- **Cost Matrix Thresholding:** Standard default threshold of 0.5 is naive for churn. We implemented a dynamic threshold that minimizes a defined cost function: $C = (\text{False Positives} \times \text{Discount Cost}) + (\text{False Negatives} \times \text{LTV Loss})$.
