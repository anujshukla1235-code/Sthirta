import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Batch Inference", page_icon="🗃️", layout="wide")

st.markdown("""
<style>
    .header-style { font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
    .sub-style { font-size: 16px; color: #64748b; margin-bottom: 30px; }
    .metric-card { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .metric-title { font-size: 14px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { font-size: 32px; font-weight: 800; color: #111827; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-style">🗃️ Batch Inference Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-style">Upload large customer datasets to process retention strategies at scale.</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Dataset")
    st.markdown("Upload your historical customer data (CSV) to run batch predictions using the Sthirta AI model.")
    
    uploaded_file = st.file_uploader("Drop your dataset here (.csv)", type=["csv"])
    
    if uploaded_file is not None:
        st.success("Dataset uploaded successfully! System ready for batch processing.")
        df = pd.read_csv(uploaded_file)
        
        st.markdown("**Data Preview:**")
        st.dataframe(df.head(4), use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Run Batch Predictions (Inference)", type="primary"):
            with st.spinner("Initializing XGBoost Inference Engine..."):
                # Mocking a progress bar for realism
                progress_bar = st.progress(0)
                status_text = st.empty()
                for percent_complete in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(percent_complete + 1)
                    status_text.text(f"Processing {len(df):,} records... {percent_complete + 1}%")
                
                status_text.empty()
                progress_bar.empty()
                
                st.success(f"✅ Successfully processed {len(df):,} customer records in 2.14s")
                
                st.markdown("---")
                st.markdown("### 📊 Inference Results Summary")
                
                # Show mock results
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-title">Total Processed</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-title">High Risk Detected</div><div class="metric-value" style="color: #DC2626;">{int(len(df) * 0.265):,}</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="metric-card"><div class="metric-title">Revenue at Risk</div><div class="metric-value" style="color: #DC2626;">${int(len(df) * 0.265 * 75):,}</div></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.info("💡 **Next Step:** Go to 'Global Business Analytics' to view macro trends, or 'Single Customer Analysis' to drill down into individual SHAP values.")

with col2:
    st.markdown("### ℹ️ Instructions")
    st.info("""
    **Accepted Format:** CSV Files only.
    
    **Required Columns:**
    - customerID
    - tenure
    - MonthlyCharges
    - TotalCharges
    - Contract
    - TechSupport
    - InternetService
    
    *Max file size: 200MB*
    """)
