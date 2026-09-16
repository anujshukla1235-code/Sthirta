import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
import os

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_churn_model.pkl")

def generate_synthetic_telco_data(n_samples=2000):
    """
    Generates a small, realistic synthetic dataset so it runs instantly on an i3 processor.
    """
    np.random.seed(42)
    
    # Features
    tenure = np.random.randint(1, 72, n_samples)
    monthly_charges = np.random.uniform(20.0, 120.0, n_samples)
    total_charges = tenure * monthly_charges * np.random.uniform(0.9, 1.1, n_samples)
    
    # Categorical features (encoded as integers for simplicity)
    contract_type = np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.3, 0.2]) # 0: Month-to-month, 1: One year, 2: Two year
    tech_support = np.random.choice([0, 1], n_samples, p=[0.7, 0.3]) # 0: No, 1: Yes
    internet_service = np.random.choice([0, 1, 2], n_samples, p=[0.2, 0.4, 0.4]) # 0: No, 1: DSL, 2: Fiber optic
    
    # Create DataFrame
    df = pd.DataFrame({
        'Tenure_Months': tenure,
        'Monthly_Charges': monthly_charges,
        'Total_Charges': total_charges,
        'Contract_Type': contract_type,
        'Tech_Support': tech_support,
        'Internet_Service': internet_service
    })
    
    # Generate Target (Churn) based on rules to make it realistic
    # Higher chance of churn if month-to-month, high charges, and no tech support
    churn_prob = (
        (df['Contract_Type'] == 0) * 0.4 +
        (df['Tech_Support'] == 0) * 0.2 +
        (df['Monthly_Charges'] > 80) * 0.2 +
        (df['Tenure_Months'] < 12) * 0.2
    )
    
    # Add some noise
    churn_prob = churn_prob + np.random.normal(0, 0.1, n_samples)
    df['Churn'] = (churn_prob > 0.5).astype(int)
    
    return df

def train_and_save_model():
    """
    Trains an ultra-lightweight XGBoost model and saves it.
    Optimized for low-RAM machines.
    """
    print("Generating dataset...")
    df = generate_synthetic_telco_data(n_samples=2000)
    
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    # Ultra-lightweight XGBoost (only 50 trees, max depth 3) -> Trains in 0.1 seconds
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    model.fit(X, y)
    
    # Save the model
    print(f"Saving model to {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)
    
    return model, X

def predict_with_explanation(customer_data_dict):
    """
    Takes a single customer's data, predicts churn, and returns SHAP values for explanation.
    """
    if not os.path.exists(MODEL_PATH):
        model, _ = train_and_save_model()
    else:
        model = joblib.load(MODEL_PATH)
        
    df_customer = pd.DataFrame([customer_data_dict])
    
    # Predict
    churn_prob = model.predict_proba(df_customer)[0][1]
    is_churn = int(churn_prob > 0.5)
    
    # SHAP Explainability (TreeExplainer is very fast for XGBoost)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df_customer)
    
    # Map SHAP values to feature names for the UI
    feature_importance = dict(zip(df_customer.columns, shap_values[0]))
    
    # Determine the top reason for churn (Feature with highest positive SHAP value)
    top_churn_driver = max(feature_importance, key=feature_importance.get) if churn_prob > 0.5 else None
    
    return {
        "churn_probability": float(churn_prob),
        "is_churn": is_churn,
        "shap_values": feature_importance,
        "top_churn_driver": top_churn_driver
    }

if __name__ == "__main__":
    # Test run the script
    model, X = train_and_save_model()
    print("Model training complete! Fast and lightweight.")
