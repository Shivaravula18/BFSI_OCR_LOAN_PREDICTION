import streamlit as st
import pickle
import numpy as np
import pandas as pd
from scripts.ocr_preprocess import extract_text
from scripts.multi_lang_ocr import extract_and_translate
from scripts.loan_processing import predict_loan_eligibility
from scripts.expenditure_analysis import analyze_bank_statement, convert_pdf_to_csv
from scripts.document_processing import process_structured_document, process_unstructured
from scripts.stock_market_analyzer import compare_stocks  # ✅ Import for Stock Market Analysis

# ✅ Load Custom CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Load Loan Prediction Model
loan_model = pickle.load(open("models/loan_approval_model.pkl", "rb"))

# ✅ Streamlit UI
st.title("📌 OCR & Loan Prediction System")
load_css()  # ✅ Apply Custom Styling

menu = ["OCR Extraction", "Multi-Language OCR", "Bank Statement Analysis", "Loan Prediction"]
choice = st.sidebar.selectbox("🔹 Select a Feature", menu)

# ✅ OCR Extraction
if choice == "OCR Extraction":
    st.header("📜 Extract & Visualize Data from Documents")

    # 🔹 Document Type Selection
    doc_category = st.selectbox("📌 Select Document Type", ["Structured", "Semi-Structured", "Unstructured"])
    doc_options = {
        "Structured": ["Bank Statements", "Profit & Loss Statements", "Balance Sheets", "Cash Flow Statements", "Invoice"],
        "Semi-Structured": ["Stock Market Analyzer"],  # ✅ Stock Market Feature
        "Unstructured": ["CSV Clustering"]  # ✅ Clustering Feature
    }
    doc_type = st.selectbox("📌 Select Specific Document", doc_options[doc_category])

    if doc_category == "Semi-Structured" and doc_type == "Stock Market Analyzer":
        compare_stocks()  # ✅ Live Stock Analysis

    elif doc_category == "Unstructured" and doc_type == "CSV Clustering":
        uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

        if uploaded_file is not None:
            st.subheader("📊 Original Data Before Clustering")
            df = pd.read_csv(uploaded_file)
            st.write(df)

            clustered_df = process_unstructured(uploaded_file)  # ✅ Perform Clustering

            st.subheader("📊 Data After Clustering")
            st.write(clustered_df)

    else:
        uploaded_file = st.file_uploader("📂 Upload Document (Image/PDF)", type=["pdf"])

        if uploaded_file is not None:
            if doc_type == "Bank Statements":
                csv_path = convert_pdf_to_csv(uploaded_file)  # ✅ Convert PDF to CSV
                df = pd.read_csv(csv_path)  # ✅ Read converted CSV
                analyze_bank_statement(df)  # ✅ Perform Expenditure Analysis

            elif doc_category == "Structured":
                process_structured_document(uploaded_file, doc_type)

# ✅ Multi-Language OCR
elif choice == "Multi-Language OCR":
    st.header("🌍 Extract & Translate Text")
    uploaded_file = st.file_uploader("📂 Upload a file", type=["png", "jpg", "jpeg", "tiff", "pdf", "docx"])

    if uploaded_file is not None:
        extracted_text, translated_text = extract_and_translate(uploaded_file)
        st.text_area("📝 Original Text:", extracted_text, height=150)
        st.text_area("🌐 Translated Text:", translated_text, height=150)

# ✅ Bank Statement Analysis
elif choice == "Bank Statement Analysis":
    st.header("🏦 Analyze Bank Statements")
    uploaded_file = st.file_uploader("📂 Upload CSV or PDF", type=["csv", "pdf"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            csv_path = convert_pdf_to_csv(uploaded_file)  # Convert PDF to CSV
            df = pd.read_csv(csv_path)  # Read converted CSV
        else:
            df = pd.read_csv(uploaded_file)  # Read directly if CSV uploaded

        analyze_bank_statement(df)  # Perform analysis

# ✅ Loan Prediction System
elif choice == "Loan Prediction":
    st.header("💰 Predict Loan Eligibility")

    # 🔹 Core Features for Loan Prediction
    marks_10th = st.number_input("📊 10th Grade Marks (%)", min_value=0, max_value=100, step=1)
    marks_12th = st.number_input("📊 12th Grade Marks (%)", min_value=0, max_value=100, step=1)
    cgpa = st.number_input("📊 CGPA", min_value=0.0, max_value=10.0, step=0.1)
    parents_credit_score = st.number_input("📈 Parents' Credit Score", min_value=300, max_value=900, step=1)
    student_credit_score = st.number_input("📈 Student's Credit Score", min_value=300, max_value=900, step=1)
    total_assets = st.number_input("🏠 Total Assets (INR)", min_value=0)
    fixed_deposits = st.number_input("💵 Fixed Deposits (INR)", min_value=0)

    # 🔹 Exam Selection for Ranking
    exam_choice = st.selectbox("🎓 Select Exam for Ranking", ["JEE", "SAT", "CAT", "NEET"])
    selected_exam_rank = st.number_input(f"📌 Enter {exam_choice} Rank", min_value=0)

    if st.button("🚀 Predict Loan Eligibility"):
        input_data = [
            marks_10th, marks_12th, cgpa, parents_credit_score, student_credit_score,
            total_assets, fixed_deposits, selected_exam_rank
        ]

        result = predict_loan_eligibility(loan_model, input_data)

        if result["status"] == "Approved":
            st.success(f"✅ Loan Approved! Amount: ₹{result['amount']} lakh")
            st.write("🏦 **Recommended Loan Schemes:**")
            for loan in result["loans"]:
                st.write(f"🔹 {loan}")
        else:
            st.error("❌ Loan Rejected. No loan available.")
