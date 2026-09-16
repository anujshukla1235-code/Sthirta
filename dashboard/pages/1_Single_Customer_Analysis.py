import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
import base64
from fpdf import FPDF

# Ensure we can import from our local analytics package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from analytics.scoring.churn_model import predict_with_explanation

# Must be the first command
st.set_page_config(page_title="Sthirta | Enterprise Churn Intelligence", page_icon="⚡", layout="wide")

# --- Helper Function for PDF ---
def create_pdf(customer_id, risk_status, prob, ltv, driver, strategy):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')
    pdf.cell(200, 10, txt=f"Sthirta Intelligence - Customer Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Customer ID: {customer_id}", ln=True)
    pdf.cell(200, 10, txt=f"Risk Status: {risk_status} ({prob:.1f}%)", ln=True)
    pdf.cell(200, 10, txt=f"Lifetime Value: ${ltv:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Primary Churn Driver: {driver}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Recommended AI Retention Strategy:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=strategy)
    return pdf.output(dest='S').encode('latin-1')

# --- Premium Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .metric-card { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); text-align: center; transition: transform 0.2s; }
    .metric-card:hover { transform: translateY(-5px); }
    .metric-title { font-size: 14px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { font-size: 32px; font-weight: 800; color: #111827; }
    .badge-critical { background-color: #FEE2E2; color: #DC2626; padding: 6px 12px; border-radius: 9999px; font-weight: 600; font-size: 14px; }
    .badge-safe { background-color: #D1FAE5; color: #059669; padding: 6px 12px; border-radius: 9999px; font-weight: 600; font-size: 14px; }
    .strategy-box { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 6px solid #0284c7; padding: 24px; border-radius: 8px; margin-top: 20px; color: #0369a1; }
    .strategy-title { font-size: 18px; font-weight: 800; margin-bottom: 12px; color: #075985; }
    .stButton>button { width: 100%; border-radius: 8px; height: 50px; font-weight: 600; font-size: 16px; background-color: #0f172a; color: white; transition: all 0.3s; }
    .stButton>button:hover { background-color: #334155; border-color: #334155; }
    hr { margin-top: 2rem; margin-bottom: 2rem; border-color: #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 style="color: #0f172a; font-weight: 800; margin-bottom: 0;">Sthirta Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 18px;">Enterprise Customer Retention & Explainable AI Engine</p>', unsafe_allow_html=True)

st.markdown("---")

# --- Layout: Sidebar for Inputs ---
with st.sidebar:
    st.markdown("### 🔍 Customer Lookup")
    input_mode = st.radio("Input Method", ["Database Search (ID)", "Manual Parameters"])
    
    # Load Real Data for Search
    data_path = os.path.join(os.path.dirname(__file__), '../../Kaggle_Telco_Customer_Churn.csv')
    df = None
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    
    selected_customer_id = "Manual"
    
    if input_mode == "Database Search (ID)" and df is not None:
        customer_ids = df['customerID'].tolist()
        selected_customer_id = st.selectbox("Search Customer ID", options=customer_ids)
        customer_row = df[df['customerID'] == selected_customer_id].iloc[0]
        
        # Override parameters with real data
        tenure = int(customer_row['tenure'])
        monthly_charges = float(customer_row['MonthlyCharges'])
        total_charges = pd.to_numeric(customer_row['TotalCharges'], errors='coerce')
        if pd.isna(total_charges): total_charges = tenure * monthly_charges
        
        contract_type = customer_row['Contract']
        tech_support = customer_row['TechSupport'] if customer_row['TechSupport'] in ['Yes', 'No'] else 'No'
        internet_service = customer_row['InternetService']
        
        st.success(f"Data for {selected_customer_id} loaded from Database.")
    else:
        st.markdown("### ⚙️ Parameters")
        tenure = st.slider("Tenure (Months)", 1, 72, 12)
        monthly_charges = st.slider("Monthly Charges ($)", 20.0, 120.0, 75.0)
        total_charges = tenure * monthly_charges
        contract_type = st.selectbox("Contract Type", options=["Month-to-month", "One year", "Two year"])
        tech_support = st.selectbox("Tech Support", options=["No", "Yes"])
        internet_service = st.selectbox("Internet Service", options=["No", "DSL", "Fiber optic"])

# Encode mappings
contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
support_map = {"No": 0, "Yes": 1}
internet_map = {"No": 0, "DSL": 1, "Fiber optic": 2}

customer_data = {
    'Tenure_Months': tenure,
    'Monthly_Charges': monthly_charges,
    'Total_Charges': total_charges,
    'Contract_Type': contract_map.get(contract_type, 0),
    'Tech_Support': support_map.get(tech_support, 0),
    'Internet_Service': internet_map.get(internet_service, 0)
}

# --- Action Button ---
run_analysis = st.button("🚀 Execute AI Retention Analysis")

if run_analysis:
    with st.spinner("Processing through XGBoost & SHAP engines..."):
        result = predict_with_explanation(customer_data)
        
        st.markdown("---")
        st.markdown("### 📊 Executive Summary")
        
        # --- Top Metric Cards ---
        m1, m2, m3 = st.columns(3)
        prob = result['churn_probability'] * 100
        
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Customer Lifetime Value</div><div class="metric-value">${total_charges:,.2f}</div></div>', unsafe_allow_html=True)
            
        with m2:
            status_html = f'<span class="badge-critical">CRITICAL RISK ({prob:.1f}%)</span>' if result['is_churn'] else f'<span class="badge-safe">STABLE ({prob:.1f}%)</span>'
            st.markdown(f'<div class="metric-card"><div class="metric-title">Churn Probability</div><div style="margin-top: 15px;">{status_html}</div></div>', unsafe_allow_html=True)
            
        with m3:
            top_driver = result['top_churn_driver'] if result['is_churn'] else "Loyalty"
            st.markdown(f'<div class="metric-card"><div class="metric-title">Primary Driver</div><div class="metric-value" style="font-size: 24px; color: #4b5563;">{top_driver.replace("_", " ")}</div></div>', unsafe_allow_html=True)
            
        # --- Middle Section: Strategy & SHAP ---
        colA, colB = st.columns([1, 1.2])
        
        with colA:
            st.markdown("### 🎯 Recommended Business Action")
            if result['is_churn']:
                # Strategy Engine
                strategy = ""
                if top_driver == "Contract_Type" and contract_map.get(contract_type, 0) == 0:
                    strategy = "This customer is highly volatile due to their month-to-month contract. **Deploy Offer:** Send an automated email offering a 15% discount to lock in an annual contract. *Expected LTV Recovery: +$450*"
                elif top_driver == "Monthly_Charges":
                    strategy = "Price sensitivity is the primary churn driver here. **Deploy Offer:** Apply a proactive $15/mo loyalty credit for the next 3 months to bypass the friction point. *Expected LTV Recovery: +$120*"
                elif top_driver == "Tech_Support" and support_map.get(tech_support, 0) == 0:
                    strategy = "Technical frustration detected. **Deploy Action:** Have the Customer Success team schedule a free 15-minute technical audit call immediately."
                else:
                    strategy = "High risk of abandonment. **Deploy Action:** Trigger a high-priority ticket for Account Managers to execute a personalized phone check-in."
                
                st.markdown(f'<div class="strategy-box"><div class="strategy-title">Automated Retention Playbook</div><p style="font-size: 16px; line-height: 1.6;">{strategy}</p></div>', unsafe_allow_html=True)
                
                # --- PDF Download Button ---
                st.markdown("<br>", unsafe_allow_html=True)
                pdf_bytes = create_pdf(selected_customer_id, "CRITICAL RISK", prob, total_charges, top_driver.replace("_", " "), strategy)
                st.download_button(label="📥 Download Strategy Report (PDF)", data=pdf_bytes, file_name=f"churn_report_{selected_customer_id}.pdf", mime="application/pdf")
                
            else:
                st.info("🟢 Customer is in a healthy state. Focus marketing efforts on cross-selling premium tiers rather than retention discounts.")

        with colB:
            st.markdown("### 🧠 Feature Attribution (SHAP)")
            # Premium Plotly Chart
            shap_vals = result['shap_values']
            df_shap = pd.DataFrame({'Feature': list(shap_vals.keys()), 'Impact': list(shap_vals.values())})
            df_shap = df_shap.sort_values(by='Impact', ascending=True)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_shap['Impact'], y=df_shap['Feature'], orientation='h',
                marker_color=['#ef4444' if val > 0 else '#10b981' for val in df_shap['Impact']],
                text=[f"+{val:.3f}" if val > 0 else f"{val:.3f}" for val in df_shap['Impact']],
                textposition='auto', hoverinfo='none'
            ))
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#e5e7eb', zeroline=True, zerolinecolor='#9ca3af', zerolinewidth=2),
                yaxis=dict(showgrid=False), font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Please configure the customer telemetry data in the sidebar and execute the analysis to generate the report.")
