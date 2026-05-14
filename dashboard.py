# dashboard.py
# NetCredit Loan Decision Monitoring Dashboard
# Built by Vamsi Sadam

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.borrowers import borrowers, quick_decision

# ── Page config ──
st.set_page_config(
    page_title="NetCredit AI Dashboard",
    page_icon="🏦",
    layout="wide"
)

# ── Title ──
st.title("🏦 NetCredit — Agentic AI Loan Decision Dashboard")
st.markdown("**Real-time monitoring of AI-powered loan evaluation system**")
st.divider()

# ── Process all borrowers ──
data = []
for b in borrowers:
    decision = quick_decision(b)
    dti = round((b["loan_amount"] / 12) / b["monthly_income"] * 100, 1)
    data.append({
        "ID":             b["id"],
        "Name":           b["name"],
        "Credit Score":   b["credit_score"],
        "Monthly Income": b["monthly_income"],
        "Loan Amount":    b["loan_amount"],
        "Bankruptcy":     b["has_bankruptcy"],
        "Employment":     b["employment"],
        "DTI %":          dti,
        "Decision":       decision
    })

df = pd.DataFrame(data)

# ── KPI Metrics ──
total    = len(df)
approved = len(df[df["Decision"] == "APPROVE"])
review   = len(df[df["Decision"] == "REVIEW"])
rejected = len(df[df["Decision"] == "REJECT"])
avg_score = int(df["Credit Score"].mean())
approval_rate = round(approved / total * 100, 1)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Applications", total)
col2.metric("✅ Approved",  approved,  f"{round(approved/total*100)}%")
col3.metric("🔍 Review",    review,    f"{round(review/total*100)}%")
col4.metric("❌ Rejected",  rejected,  f"{round(rejected/total*100)}%")
col5.metric("Avg Credit Score", avg_score)

st.divider()

# ── Charts Row 1 ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Loan Decision Distribution")
    decision_counts = df["Decision"].value_counts().reset_index()
    decision_counts.columns = ["Decision", "Count"]
    colors = {"APPROVE": "#00CC96", "REVIEW": "#FFA15A", "REJECT": "#EF553B"}
    fig1 = px.pie(
        decision_counts,
        names="Decision",
        values="Count",
        color="Decision",
        color_discrete_map=colors,
        hole=0.4
    )
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📈 Credit Score Distribution")
    fig2 = px.histogram(
        df,
        x="Credit Score",
        color="Decision",
        nbins=20,
        color_discrete_map=colors,
        barmode="overlay"
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts Row 2 ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Loan Amount vs Credit Score")
    fig3 = px.scatter(
        df,
        x="Credit Score",
        y="Loan Amount",
        color="Decision",
        size="Monthly Income",
        hover_data=["Name", "ID", "DTI %"],
        color_discrete_map=colors
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("📉 Debt-to-Income Ratio by Decision")
    fig4 = px.box(
        df,
        x="Decision",
        y="DTI %",
        color="Decision",
        color_discrete_map=colors
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Borrower Table ──
st.subheader("📋 All Borrower Applications")

# Filter
decision_filter = st.selectbox(
    "Filter by Decision:",
    ["ALL", "APPROVE", "REVIEW", "REJECT"]
)

if decision_filter != "ALL":
    filtered_df = df[df["Decision"] == decision_filter]
else:
    filtered_df = df

# Color code decisions
def color_decision(val):
    colors_map = {
        "APPROVE": "background-color: #1a4731; color: #00CC96",
        "REVIEW":  "background-color: #4a3520; color: #FFA15A",
        "REJECT":  "background-color: #4a1a1a; color: #EF553B"
    }
    return colors_map.get(val, "")

styled_df = filtered_df.style.map(
    color_decision, subset=["Decision"]
).format({"DTI %": "{:.1f}%"})

st.dataframe(styled_df, use_container_width=True, height=400)

st.divider()

# ── Risk Summary ──
st.subheader("🎯 Risk Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ✅ APPROVE criteria")
    st.markdown("""
    - Credit score ≥ 700
    - DTI ratio < 40%
    - No bankruptcy
    - Income ≥ $2,000/month
    """)

with col2:
    st.markdown("### 🔍 REVIEW criteria")
    st.markdown("""
    - Credit score 500–699
    - DTI ratio 40–60%
    - Borderline income
    - Needs analyst review
    """)

with col3:
    st.markdown("### ❌ REJECT criteria")
    st.markdown("""
    - Credit score < 500
    - Recent bankruptcy
    - Income < $2,000/month
    - High DTI ratio
    """)

st.divider()
st.caption("Built by Vamsi Sadam | NetCredit Agentic AI System | CrewAI + GPT-4 + Streamlit")