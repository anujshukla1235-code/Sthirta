# Sthirta: Intelligent Churn & Retention Engine 📈

Most ML churn projects stop at predicting *who* will churn. **Sthirta** goes a step further: it uses Explainable AI (SHAP) to explain *why* they are leaving, and suggests a specific, actionable *retention strategy*.

## 🚀 Key Features
- **Ultra-Fast XGBoost Core:** Trained on Telco data, optimized for low-resource environments (runs instantly).
- **Explainable AI (SHAP):** Transparent predictions. See exactly which features (like high prices or lack of tech support) are pushing the customer to leave.
- **Dynamic Retention Engine:** Business-rule engine that maps AI output to actionable HR/Manager strategies (e.g., "Offer a $15 loyalty discount").
- **Full-Stack Architecture:** 
  - `FastAPI` Backend for REST API serving.
  - `Streamlit` interactive dashboard for managers.

## 🛠️ Tech Stack
- **Machine Learning:** `xgboost`, `scikit-learn`, `shap`, `pandas`
- **Backend:** `FastAPI`, `uvicorn`
- **Frontend:** `Streamlit`

## 🏃‍♂️ How to Run (Local)

1. **Activate Virtual Environment:**
   ```bash
   .\venv\Scripts\activate
   ```

2. **Run the Dashboard (UI):**
   ```bash
   streamlit run dashboard\app.py
   ```

3. **Run the API Server (Optional):**
   ```bash
   uvicorn backend.app.main:app --reload
   ```

## 📁 SDLC Compliance
This project strictly follows the Agile methodology defined in the `docs/` folder, meeting all KPIs outlined in the Vision Charter (Recall optimization, SHAP integration, and segmented retention).
