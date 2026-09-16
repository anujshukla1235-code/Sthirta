import streamlit as st

st.set_page_config(page_title="Welcome to Sthirta", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .welcome-header { font-size: 52px; font-weight: 900; color: #0f172a; margin-bottom: 0px; letter-spacing: -1px; }
    .welcome-sub { font-size: 22px; color: #64748b; margin-bottom: 50px; font-weight: 400; }
    .feature-card { padding: 30px; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); height: 100%; transition: transform 0.2s; }
    .feature-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
    .feature-icon { font-size: 40px; margin-bottom: 15px; }
    .feature-title { font-size: 20px; font-weight: 700; color: #1e293b; margin-bottom: 10px; }
    .feature-desc { font-size: 15px; color: #64748b; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="welcome-header">Sthirta Intelligence ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-sub">The Enterprise Customer Retention & Explainable AI Engine</div>', unsafe_allow_html=True)
st.markdown("---")

st.markdown("### 🚀 Welcome to your Workspace")
st.markdown("Sthirta goes beyond traditional Machine Learning. Instead of just predicting *who* will churn, it uses **Game Theory (SHAP)** to tell you exactly *why* they are leaving, and generates automated business strategies to retain them.")
st.markdown("<br>", unsafe_allow_html=True)

# Feature Grid
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">1. Single Customer Analysis</div>
        <div class="feature-desc">Search for specific customers or simulate parameters. Get real-time SHAP feature attribution and automated retention playbooks (Exportable to PDF).</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">2. Global Business Analytics</div>
        <div class="feature-desc">View macro-level insights. Understand historical churn rates, revenue lost to churn, and demographic distributions across your entire active user base.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗃️</div>
        <div class="feature-title">3. Batch Inference Engine</div>
        <div class="feature-desc">Upload large-scale customer datasets (CSV) to process thousands of records simultaneously and identify your highest-risk revenue segments.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.info("👈 **Please select a module from the sidebar on the left to begin your analysis.**")
