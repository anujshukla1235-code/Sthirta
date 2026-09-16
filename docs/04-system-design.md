# 04 - System Design Document: Churn Prediction with Explainability & Retention Strategy

## High-Level Architecture

```
[Data Source] --> [Preprocessing/Feature Pipeline] --> [Model/Logic Core]
                                                            |
                                                            v
                                              [Serving Layer: API/App]
                                                            |
                                                            v
                                                   [User-Facing Dashboard]
```

## Tech Stack
- Python
- scikit-learn/XGBoost
- SHAP
- Streamlit
- pandas

## Data Flow
1. Raw data ingested from source (Telco Customer Churn dataset (Kaggle) or a SaaS-style synthetic dataset).
2. Cleaned and feature-engineered in the preprocessing stage.
3. Model/logic core trained (or invoked, for the LLM-based/no-dataset projects) and validated against the Test Plan.
4. Predictions/outputs served via API or app layer.
5. Results rendered in an interactive dashboard for the end user.

## Key Design Decisions
- **Adds a 'why + what to do' layer: SHAP-based per-customer explanation, automatic customer segmentation, and a mapped retention action per segment (e.g. discount, support outreach) with estimated cost-benefit.** — this is the core differentiator and should be reflected in the architecture, not bolted on at the end.
- Keep the preprocessing and model logic decoupled from the UI layer so either can be swapped/tested independently.

## Non-Functional Requirements
- Reasonable latency for interactive use (see KPIs in doc 01)
- Reproducibility: pipeline runnable end-to-end from a single script/notebook
- Clear separation of config (paths, hyperparameters) from code
