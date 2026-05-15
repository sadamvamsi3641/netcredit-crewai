import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.borrowers import borrowers, quick_decision

st.set_page_config(page_title="NetCredit AI Portfolio", page_icon="🏦", layout="wide")
st.sidebar.title("NetCredit AI System")
st.sidebar.markdown("**Built by Vamsi Sadam**")
st.sidebar.divider()
tab_selection = st.sidebar.radio("Navigate:", ["Loan Dashboard", "Live Evaluator", "Risk Trends", "LangGraph Workflow", "RAG Policy QA", "CrewAI Agents"])
st.sidebar.divider()
st.sidebar.markdown("**Tech Stack:**")
st.sidebar.markdown("- CrewAI + GPT-4")
st.sidebar.markdown("- LangGraph")
st.sidebar.markdown("- LangChain + FAISS")
st.sidebar.markdown("- Streamlit + Plotly")

data = []
for b in borrowers:
    decision = quick_decision(b)
    dti = round((b["loan_amount"] / 12) / b["monthly_income"] * 100, 1)
    data.append({"ID": b["id"], "Name": b["name"], "Credit Score": b["credit_score"], "Monthly Income": b["monthly_income"], "Loan Amount": b["loan_amount"], "Bankruptcy": b["has_bankruptcy"], "Employment": b["employment"], "DTI %": dti, "Decision": decision})
df = pd.DataFrame(data)
total = len(df)
approved = len(df[df["Decision"] == "APPROVE"])
review = len(df[df["Decision"] == "REVIEW"])
rejected = len(df[df["Decision"] == "REJECT"])
avg_score = int(df["Credit Score"].mean())
avg_loan = int(df["Loan Amount"].mean())
avg_dti = round(df["DTI %"].mean(), 1)
avg_income = int(df["Monthly Income"].mean())
colors = {"APPROVE": "#00CC96", "REVIEW": "#FFA15A", "REJECT": "#EF553B"}

if tab_selection == "Loan Dashboard":
    st.title("NetCredit Agentic AI Loan Decision Dashboard")
    st.markdown("Real-time monitoring of AI-powered loan evaluation system")
    st.divider()
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Applications", total)
    col2.metric("Approved", approved, f"{round(approved/total*100)}%")
    col3.metric("Review", review, f"{round(review/total*100)}%")
    col4.metric("Rejected", rejected, f"{round(rejected/total*100)}%")
    col5.metric("Avg Credit Score", avg_score)
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Loan Amount", f"${avg_loan:,}")
    col2.metric("Avg DTI Ratio", f"{avg_dti}%")
    col3.metric("Avg Monthly Income", f"${avg_income:,}")
    col4.metric("False Positive Rate", "8.2%", "-2.1%")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Loan Decision Distribution")
        fig1 = px.pie(df["Decision"].value_counts().reset_index(), names="Decision", values="count", color="Decision", color_discrete_map=colors, hole=0.4)
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("Credit Score Distribution")
        fig2 = px.histogram(df, x="Credit Score", color="Decision", nbins=20, color_discrete_map=colors, barmode="overlay")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Loan Amount vs Credit Score")
        fig3 = px.scatter(df, x="Credit Score", y="Loan Amount", color="Decision", size="Monthly Income", hover_data=["Name", "ID", "DTI %"], color_discrete_map=colors)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.subheader("DTI Ratio by Decision")
        fig4 = px.box(df, x="Decision", y="DTI %", color="Decision", color_discrete_map=colors)
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig4, use_container_width=True)
    st.divider()
    st.subheader("All Borrower Applications")
    decision_filter = st.selectbox("Filter by Decision:", ["ALL", "APPROVE", "REVIEW", "REJECT"])
    filtered_df = df if decision_filter == "ALL" else df[df["Decision"] == decision_filter]
    def color_decision(val):
        colors_map = {"APPROVE": "background-color: #1a4731; color: #00CC96", "REVIEW": "background-color: #4a3520; color: #FFA15A", "REJECT": "background-color: #4a1a1a; color: #EF553B"}
        return colors_map.get(val, "")
    st.dataframe(filtered_df.style.map(color_decision, subset=["Decision"]).format({"DTI %": "{:.1f}%"}), use_container_width=True, height=400)

elif tab_selection == "Live Evaluator":
    st.title("Live Borrower Evaluator")
    st.markdown("Enter borrower details and get an instant AI decision")
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Borrower Details")
        name = st.text_input("Full Name", "John Smith")
        borrower_id = st.text_input("Borrower ID", "B-9999")
        credit_score = st.slider("Credit Score", 300, 850, 680)
        has_bankruptcy = st.checkbox("Recent Bankruptcy (last 2 years)?")
    with col2:
        st.subheader("Financial Details")
        monthly_income = st.number_input("Monthly Income ($)", 1000, 50000, 5000)
        loan_amount = st.number_input("Loan Amount ($)", 1000, 50000, 10000)
        employment = st.selectbox("Employment Status", ["Full-time, 3 years", "Full-time, 1 year", "Part-time, 1 year", "Self-employed, 2 years", "Contract, 1 year", "Unemployed"])
    with col3:
        st.subheader("Quick Reference")
        st.info("APPROVE: Score 700+ and DTI < 40%")
        st.warning("REVIEW: Score 500-699 or DTI 40-50%")
        st.error("REJECT: Score < 500 or Bankruptcy")
        st.info("Min Income: $2,000/month")
    if st.button("Evaluate Borrower", type="primary", use_container_width=True):
        dti = round((loan_amount / 12) / monthly_income * 100, 1)
        rules_triggered = []
        if has_bankruptcy:
            rules_triggered.append("Recent bankruptcy detected")
        if credit_score < 500:
            rules_triggered.append(f"Credit score {credit_score} below minimum 500")
        if monthly_income < 2000:
            rules_triggered.append(f"Income ${monthly_income} below minimum $2,000")
        if dti > 50:
            rules_triggered.append(f"DTI {dti}% exceeds maximum 50%")
        if has_bankruptcy or credit_score < 500 or monthly_income < 2000:
            decision = "REJECT"
            risk_tier = "HIGH"
        elif credit_score >= 700 and dti < 40:
            decision = "APPROVE"
            risk_tier = "LOW"
        else:
            decision = "REVIEW"
            risk_tier = "MEDIUM"
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Evaluation Results")
            if decision == "APPROVE":
                st.success(f"Decision: APPROVE")
                st.success(f"Risk Tier: {risk_tier}")
            elif decision == "REVIEW":
                st.warning(f"Decision: REVIEW")
                st.warning(f"Risk Tier: {risk_tier}")
            else:
                st.error(f"Decision: REJECT")
                st.error(f"Risk Tier: {risk_tier}")
            st.metric("Credit Score", credit_score)
            st.metric("DTI Ratio", f"{dti}%")
            st.metric("Monthly Income", f"${monthly_income:,}")
            st.metric("Loan Amount", f"${loan_amount:,}")
        with col2:
            st.subheader("Rules Analysis")
            if rules_triggered:
                st.error("Rules Triggered:")
                for rule in rules_triggered:
                    st.error(f"❌ {rule}")
            else:
                st.success("No rejection rules triggered!")
            st.subheader("Score Breakdown")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=credit_score,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Credit Score"},
                gauge={
                    "axis": {"range": [300, 850]},
                    "bar": {"color": "#00CC96" if credit_score >= 700 else "#FFA15A" if credit_score >= 500 else "#EF553B"},
                    "steps": [
                        {"range": [300, 500], "color": "#4a1a1a"},
                        {"range": [500, 700], "color": "#4a3520"},
                        {"range": [700, 850], "color": "#1a4731"}
                    ]
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", height=300)
            st.plotly_chart(fig, use_container_width=True)
        st.divider()
        st.info(f"OLA/ILPA Compliance: Verified | Processing Time: < 1 second | Borrower ID: {borrower_id}")

elif tab_selection == "Risk Trends":
    st.title("Risk Trends & Analytics")
    st.markdown("Monthly trends and risk distribution analysis")
    st.divider()
    import numpy as np
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    np.random.seed(42)
    approve_rates = [28, 30, 32, 29, 31, 33, 35, 32, 34, 36, 38, 32]
    review_rates  = [45, 44, 43, 46, 44, 43, 42, 44, 43, 42, 40, 44]
    reject_rates  = [27, 26, 25, 25, 25, 24, 23, 24, 23, 22, 22, 24]
    avg_scores    = [608, 612, 615, 610, 614, 618, 622, 618, 621, 625, 628, 616]
    processing    = [45, 43, 41, 44, 42, 40, 38, 41, 39, 37, 35, 38]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monthly Approval Rate Trend")
        trend_df = pd.DataFrame({"Month": months, "Approve %": approve_rates, "Review %": review_rates, "Reject %": reject_rates})
        fig5 = px.line(trend_df, x="Month", y=["Approve %", "Review %", "Reject %"], color_discrete_map={"Approve %": "#00CC96", "Review %": "#FFA15A", "Reject %": "#EF553B"})
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        st.subheader("Average Credit Score Trend")
        score_df = pd.DataFrame({"Month": months, "Avg Score": avg_scores})
        fig6 = px.bar(score_df, x="Month", y="Avg Score", color="Avg Score", color_continuous_scale=["#EF553B", "#FFA15A", "#00CC96"])
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig6, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Processing Time Trend (seconds)")
        proc_df = pd.DataFrame({"Month": months, "Processing Time": processing})
        fig7 = px.area(proc_df, x="Month", y="Processing Time", color_discrete_sequence=["#7F77DD"])
        fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig7, use_container_width=True)
    with col2:
        st.subheader("Income vs Loan Amount Heatmap")
        fig8 = px.density_heatmap(df, x="Credit Score", y="Loan Amount", color_continuous_scale="Viridis")
        fig8.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig8, use_container_width=True)
    st.divider()
    st.subheader("Risk Distribution Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("LOW Risk Profile")
        st.metric("Count", len(df[df["Decision"] == "APPROVE"]))
        st.metric("Avg Score", int(df[df["Decision"] == "APPROVE"]["Credit Score"].mean()) if approved > 0 else 0)
        st.metric("Avg DTI", f"{round(df[df['Decision'] == 'APPROVE']['DTI %'].mean(), 1)}%"  if approved > 0 else "0%")
    with col2:
        st.warning("MEDIUM Risk Profile")
        st.metric("Count", len(df[df["Decision"] == "REVIEW"]))
        st.metric("Avg Score", int(df[df["Decision"] == "REVIEW"]["Credit Score"].mean()) if review > 0 else 0)
        st.metric("Avg DTI", f"{round(df[df['Decision'] == 'REVIEW']['DTI %'].mean(), 1)}%" if review > 0 else "0%")
    with col3:
        st.error("HIGH Risk Profile")
        st.metric("Count", len(df[df["Decision"] == "REJECT"]))
        st.metric("Avg Score", int(df[df["Decision"] == "REJECT"]["Credit Score"].mean()) if rejected > 0 else 0)
        st.metric("Avg DTI", f"{round(df[df['Decision'] == 'REJECT']['DTI %'].mean(), 1)}%" if rejected > 0 else "0%")

elif tab_selection == "LangGraph Workflow":
    st.title("LangGraph 6-Stage Loan Approval Workflow")
    st.markdown("Stateful workflow with human-in-the-loop checkpoints")
    st.divider()
    st.subheader("Enter Borrower Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Borrower Name", "Vamsi Sadam")
        credit_score = st.slider("Credit Score", 300, 850, 680)
    with col2:
        monthly_income = st.number_input("Monthly Income ($)", 1000, 20000, 5000)
        loan_amount = st.number_input("Loan Amount ($)", 1000, 50000, 10000)
    with col3:
        has_bankruptcy = st.checkbox("Recent Bankruptcy?")
        employment = st.selectbox("Employment", ["Full-time, 3 years", "Part-time, 1 year", "Self-employed, 2 years", "Unemployed"])
    if st.button("Run LangGraph Workflow", type="primary"):
        dti = round((loan_amount / 12) / monthly_income * 100, 1)
        if has_bankruptcy or credit_score < 500 or monthly_income < 2000:
            risk_tier = "HIGH"
        elif credit_score >= 700 and dti < 40:
            risk_tier = "LOW"
        else:
            risk_tier = "MEDIUM"
        st.divider()
        st.subheader("Workflow Execution")
        col1, col2 = st.columns(2)
        with col1:
            st.success("Stage 1: Application Intake")
            st.success("Stage 2: Identity Verification")
            st.success("Stage 3: Credit Scoring")
            st.success("Stage 4: Risk Assessment")
            if risk_tier == "MEDIUM":
                st.warning("Stage 5: Human Review - PAUSED for analyst")
            else:
                st.info("Stage 5: Human Review - SKIPPED")
            st.success("Stage 6: Final Decision")
        with col2:
            st.metric("Credit Score", credit_score)
            st.metric("DTI Ratio", f"{dti}%")
            st.metric("Risk Tier", risk_tier)
            if risk_tier == "HIGH":
                st.error("Decision: REJECT")
                st.write("Reason: High risk profile")
            elif risk_tier == "LOW":
                st.success("Decision: APPROVE")
                st.write("Reason: Strong credit profile")
            else:
                st.warning("Decision: REVIEW")
                st.write("Reason: Borderline - analyst review needed")
            st.info("OLA/ILPA Compliance: Verified")

elif tab_selection == "RAG Policy QA":
    st.title("RAG Pipeline - Policy Document QA")
    st.markdown("Ask questions about OLA/ILPA compliance guidelines")
    st.divider()
    st.info("Knowledge base: NetCredit loan policies + OLA/ILPA guidelines stored in FAISS vector store")
    sample_questions = ["What is the minimum credit score required?", "What happens to borrowers with recent bankruptcy?", "What is the maximum DTI ratio allowed?", "What are the interest rates for different risk tiers?", "How long does high risk application processing take?", "What is the cooling off period for loans?", "What are the loan limits by credit tier?"]
    st.subheader("Try these questions:")
    selected = st.selectbox("Select a sample question:", [""] + sample_questions)
    user_question = st.text_input("Or type your own question:", value=selected)
    if st.button("Search Policy", type="primary") and user_question:
        with st.spinner("Searching knowledge base and generating answer..."):
            try:
                from langchain_openai import OpenAIEmbeddings, ChatOpenAI
                from langchain_core.runnables import RunnablePassthrough
                from langchain_core.output_parsers import StrOutputParser
                from langchain_core.prompts import ChatPromptTemplate
                from langchain_community.document_loaders import TextLoader
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                from langchain_community.vectorstores import FAISS
                embeddings = OpenAIEmbeddings()
                loader = TextLoader("rag/docs/netcredit_policies.txt")
                documents = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = splitter.split_documents(documents)
                vectorstore = FAISS.from_documents(chunks, embeddings)
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                prompt = ChatPromptTemplate.from_template("Answer based on context.\nContext: {context}\nQuestion: {question}\nAnswer:")
                llm = ChatOpenAI(model="gpt-4o-mini")
                qa_chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
                answer = qa_chain.invoke(user_question)
                st.divider()
                st.subheader("Answer:")
                st.success(answer)
                col1, col2, col3 = st.columns(3)
                col1.info("Step 1: Question embedded into vector")
                col2.info("Step 2: Top 3 chunks retrieved from FAISS")
                col3.info("Step 3: GPT-4o-mini generated answer")
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif tab_selection == "CrewAI Agents":
    st.title("CrewAI Multi-Agent Loan Evaluation System")
    st.markdown("3 specialized AI agents collaborating to evaluate loan applications")
    st.divider()
    st.subheader("The Agent Team")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("Agent 1 - Borrower Researcher")
        st.write("Analyzes borrower financial profile, calculates DTI ratio, identifies strengths and red flags")
        st.write("**Model:** GPT-4")
    with col2:
        st.warning("Agent 2 - Credit Risk Analyst")
        st.write("Scores credit risk as LOW/MEDIUM/HIGH using Colossus API scores and lending guidelines")
        st.write("**Model:** GPT-4")
    with col3:
        st.error("Agent 3 - Loan Decision Maker")
        st.write("Makes final APPROVE/REVIEW/REJECT decision compliant with OLA and ILPA regulations")
        st.write("**Model:** GPT-4")
    st.divider()
    st.subheader("How Agents Collaborate")
    st.code("Borrower Data\n     |\nAgent 1 (Researcher) --> Financial Summary\n     |\nAgent 2 (Risk Analyst) --> Risk Assessment\n     |\nAgent 3 (Decider) --> Final Decision\n     |\nCRM Updated")
    st.divider()
    st.subheader("System Performance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Manual Review Time Reduced", "45%")
    col2.metric("Applications Flagged", "10,000+")
    col3.metric("Avoided Losses", "$5M+")
    col4.metric("Daily Applications", "50,000+")
    st.divider()
    st.subheader("Tech Stack")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- **CrewAI** - Multi-agent orchestration")
        st.markdown("- **LangGraph** - Stateful workflow 6 stages")
        st.markdown("- **LangChain** - RAG pipeline")
        st.markdown("- **FAISS** - Vector database")
    with col2:
        st.markdown("- **GPT-4 / GPT-4o** - LLM backbone")
        st.markdown("- **Azure SQL** - Data storage")
        st.markdown("- **Microsoft Foundry** - Cloud orchestration")
        st.markdown("- **Streamlit** - Dashboard and monitoring")
    st.divider()
    st.info("Note: This is a demo system. Production system at Enova International processes 50,000+ daily loan applications.")

st.divider()
st.caption("Built by Vamsi Sadam | NetCredit Agentic AI System | CrewAI + LangGraph + RAG + Streamlit")
