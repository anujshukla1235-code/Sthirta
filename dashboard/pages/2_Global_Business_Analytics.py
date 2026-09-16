import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Global Business Analytics", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .metric-card { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .metric-title { font-size: 14px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { font-size: 32px; font-weight: 800; color: #111827; }
    .danger { color: #DC2626; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Global Business Analytics")
st.markdown("Macro-level insights into customer behavior, revenue at risk, and historical churn trends.")
st.markdown("---")

# Try to load the Kaggle dataset
data_path = os.path.join(os.path.dirname(__file__), '../../Kaggle_Telco_Customer_Churn.csv')

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    # Calculate top level metrics
    total_customers = len(df)
    total_churned = len(df[df['Churn'] == 'Yes'])
    churn_rate = (total_churned / total_customers) * 100
    
    # Clean TotalCharges (some are empty strings)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    revenue_lost = df[df['Churn'] == 'Yes']['TotalCharges'].sum()
    
    # --- Top Metrics ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Active Base</div><div class="metric-value">{total_customers:,}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Historical Churn Rate</div><div class="metric-value danger">{churn_rate:.1f}%</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Revenue Lost to Churn</div><div class="metric-value danger">${revenue_lost:,.0f}</div></div>', unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # --- Charts ---
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("#### Churn by Contract Type")
        contract_churn = df.groupby(['Contract', 'Churn']).size().reset_index(name='Count')
        fig1 = px.bar(contract_churn, x='Contract', y='Count', color='Churn', barmode='group', 
                      color_discrete_map={'Yes': '#ef4444', 'No': '#10b981'})
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        
    with colB:
        st.markdown("#### Density of Churn by Monthly Charges")
        fig2 = px.histogram(df, x="MonthlyCharges", color="Churn", marginal="box", 
                            color_discrete_map={'Yes': '#ef4444', 'No': '#10b981'}, nbins=30)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        
    # --- Bottom Chart ---
    st.markdown("#### Tenure vs Churn (Survival Insight)")
    fig3 = px.box(df, x="Churn", y="tenure", color="Churn", color_discrete_map={'Yes': '#ef4444', 'No': '#10b981'})
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("⚠️ Kaggle Dataset not found. Please go to the Welcome Page and upload 'Kaggle_Telco_Customer_Churn.csv' to enable Global Analytics.")
