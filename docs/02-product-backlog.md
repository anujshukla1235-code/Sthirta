# 02 - Product Backlog: Churn Prediction with Explainability & Retention Strategy

## Epics & User Stories

| # | Epic | User Story | Acceptance Criteria | Priority (MoSCoW) |
|---|------|------------|----------------------|--------------------|
| 1 | Data prep | As a user, I want cleaned customer data so that the model trains correctly. | No nulls in numeric features, categorical encoding validated. | Must |
| 2 | Churn model | As a user, I want a churn classifier so that I can identify at-risk customers. | Model trained, precision/recall reported, threshold justified. | Must |
| 3 | Explainability | As a retention manager, I want SHAP explanations per customer so that I understand WHY they'll churn. | SHAP waterfall plot generated per selected customer. | Should |
| 4 | Segmentation | As a retention manager, I want customers grouped by churn-driver so that I can target strategies. | At least 3 segments identified with distinct top SHAP features. | Should |
| 5 | Retention dashboard | As a user, I want an interactive dashboard so that I can explore churners and recommended actions. | Streamlit app: search customer, see risk score, SHAP plot, recommended action. | Could |

## Backlog Grooming Notes
- Re-prioritize at the start of each sprint based on progress and blockers.
- "Must" items are required for a demo-able v1. "Should"/"Could" items are enhancements for later sprints or a v2.
- Add new stories as they surface during development rather than trying to define everything upfront (Agile principle).
