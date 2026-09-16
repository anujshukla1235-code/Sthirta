# 05 - Test Plan: Churn Prediction with Explainability & Retention Strategy

## Test Levels
1. **Unit tests** - individual functions (data cleaning, feature engineering, formula/metric calculations)
2. **Integration tests** - pipeline stages working together (data -> features -> model -> output)
3. **Validation tests** - domain-specific correctness (see focus area below)
4. **UI/acceptance tests** - manual walkthrough of each user story's acceptance criteria (doc 02)

## Project-Specific Test Focus
Model evaluation on stratified k-fold, SHAP value sanity checks (sum equals prediction), segmentation stability across runs, dashboard input validation.

## Sample Test Cases

| ID | Description | Type | Expected Result |
|----|-------------|------|------------------|
| TC-01 | Pipeline runs end-to-end on sample data | Integration | Completes without error, output shape correct |
| TC-02 | Model/logic output validated against a known baseline | Validation | Output beats or matches baseline per KPI in doc 01 |
| TC-03 | Edge case: empty/malformed input | Unit | Graceful error/handled fallback, no crash |
| TC-04 | UI loads and core interaction works | Acceptance | Matches acceptance criteria from doc 02 |

## Tools
pytest (unit/integration), manual checklist (acceptance), project-specific validation libraries noted in doc 04's tech stack.
