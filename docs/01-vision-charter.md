# 01 - Vision & Charter: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## Problem Statement
Customer churn in the Telecom/SaaS industry costs organizations millions annually in lost recurring revenue. According to industry data, acquiring a new customer can cost 5-25 times more than retaining an existing one. While many machine learning initiatives successfully predict *who* will churn, they often fail to explain *why* or prescribe *what to do* about it. Without actionable, segment-specific retention strategies mapped to clear cost-benefit thresholds, customer success teams are left guessing, often applying expensive discounts to customers who don't need them or missing the chance to save those who do.

## Scope
**Inclusions:**
- End-to-end data pipeline with automated PII masking.
- XGBoost churn classification model trained on Telecom/SaaS data.
- SHAP TreeExplainer integration for per-customer explainability, with offline pre-computation and caching (Parquet/SQLite).
- Cost-benefit threshold optimization (Cost Matrix for False Positives vs. False Negatives).
- Interactive Retention Dashboard on Streamlit Community Cloud.
- Batch inference export (CSV) for CRM synchronization.
- Feedback loop tracking to measure the efficacy of applied retention actions.

**Exclusions:**
- Real-time streaming data ingestion (v1 focuses on batch processing).
- Direct bi-directional API integration with third-party CRMs (handled via CSV export).
- Deep learning/Neural Network approaches (XGBoost is prioritized for explainability).

## Target Personas
- **Customer Success Manager:** Needs to know which accounts to prioritize and the precise reason for their churn risk to tailor conversations.
- **Retention Marketing Lead:** Requires segmented groups to design targeted promotional campaigns based on the top churn drivers.
- **VP Revenue:** Needs visibility into the overall financial impact of predicted churn and the ROI of retention strategies.
- **ML Engineer:** Responsible for model training, SHAP value caching, and maintaining pipeline health.

## Stakeholders
- **Chief Revenue Officer (CRO)**
- **Customer Success Team**
- **Marketing Analytics Lead**
- **Data Engineering**

## Success Metrics (Quantitative KPIs)
- **Recall on churners:** > 80%
- **Precision:** > 65%
- **F1 Score:** > 72%
- **Explainability Latency:** SHAP computation and rendering < 2s per customer (via cached Parquet/SQLite layer).

## Risk Assessment
- **Data Leakage Risk:** High. Target variables could inadvertently bleed into training data. Mitigation: Strict temporal splits and pipeline isolation.
- **Compute Bottleneck Risk:** SHAP TreeExplainer is computationally expensive at scale. Mitigation: Pre-computing SHAP values offline and serving from a fast cache layer.
- **Concept Drift Risk:** Customer behavior changes over time, rendering the model stale. Mitigation: Implementing PSI (Population Stability Index) and Evidently AI for automated drift detection.
- **Privacy Risk:** Exposure of customer PII in the dashboard. Mitigation: Enforced PII masking at the ingestion layer.
