import pdfplumber
import cv2
import pytesseract
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re
import os
from sklearn.cluster import KMeans
from scripts.expenditure_analysis import analyze_bank_statement
from scripts.stock_market_analyzer import compare_stocks  # ✅ Semi-Structured Data Processing

# ✅ Extract Text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# ✅ Extract Text from Images (Unstructured Data - Cheques)
def extract_text_from_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return pytesseract.image_to_string(thresh)

# ✅ Structured Data Processing (Bank Statements, P&L, Balance Sheet, Cash Flow, Invoice)
def process_structured_document(uploaded_file, doc_type):
    extracted_text = extract_text_from_pdf(uploaded_file)
    structured_data = {}

    if doc_type == "Bank Statements":
        df = analyze_bank_statement(extracted_text)
        return df.to_dict()

    elif doc_type == "Balance Sheets":
        structured_data = extract_balance_sheet_data(extracted_text)
        visualize_balance_sheet(structured_data)

    elif doc_type == "Profit & Loss Statements":
        structured_data = extract_profit_loss_data(extracted_text)
        visualize_profit_loss(structured_data)

    elif doc_type == "Cash Flow Statements":
        structured_data = extract_cash_flow_data(extracted_text)
        visualize_cash_flow(structured_data)

    elif doc_type == "Invoice":
        structured_data = extract_invoice_data(extracted_text)
        visualize_invoice_data(structured_data)

    return structured_data

# ✅ Semi-Structured Data Processing (Stock Market Analysis)
def process_semi_structured():
    compare_stocks()

# ✅ Unstructured Data Processing (CSV Clustering) - FIXED ERROR!
def process_unstructured(uploaded_file):
    try:
        st.subheader("📂 Uploaded CSV Data (Before Clustering)")

        # ✅ Save the uploaded file to a temporary location
        with open("temp_uploaded_file.csv", "wb") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
        
        file_path = "temp_uploaded_file.csv"

        # ✅ Read the file as a DataFrame
        df = pd.read_csv(file_path)

        # ✅ Check if CSV has data
        if df.empty:
            st.error("⚠️ The uploaded CSV file is empty. Please upload a valid CSV file.")
            return None

        st.write("✅ Successfully Loaded CSV Data", df.head())

        # ✅ Select only numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            st.error("⚠️ The CSV file must have at least two numeric columns for clustering.")
            return None

        # ✅ User selects features for clustering
        feature_x = st.selectbox("🔹 Select X-axis Feature", numeric_cols, index=0)
        feature_y = st.selectbox("🔹 Select Y-axis Feature", numeric_cols, index=1)

        # ✅ Apply K-Means Clustering
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df["Cluster"] = kmeans.fit_predict(df[[feature_x, feature_y]])

        st.subheader("📊 Clustered Data (After Clustering)")
        st.write(df)

        # ✅ Visualization of Clustering
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x=feature_x, y=feature_y, hue="Cluster", palette="viridis", s=100)
        plt.title(f"K-Means Clustering: {feature_x} vs. {feature_y}")
        plt.xlabel(feature_x)
        plt.ylabel(feature_y)
        plt.legend(title="Cluster")
        st.pyplot(plt)

        return df

    except pd.errors.EmptyDataError:
        st.error("⚠️ The uploaded CSV file is empty or corrupted. Please upload a valid file.")
    except Exception as e:
        st.error(f"⚠️ Error processing CSV file: {e}")
    finally:
        if os.path.exists("temp_uploaded_file.csv"):
            os.remove("temp_uploaded_file.csv")

# ✅ Balance Sheet Extraction
def extract_balance_sheet_data(text):
    extracted_data = {
        "Total Assets": extract_value(r"Total Assets[\s\S]*?(\d{1,3}(?:,\d{3})*)", text),
        "Total Liabilities": extract_value(r"Total Liabilities[\s\S]*?(\d{1,3}(?:,\d{3})*)", text),
        "Fixed Assets": extract_value(r"Fixed Assets[\s\S]*?(\d{1,3}(?:,\d{3})*)", text),
    }
    return extracted_data

# ✅ Profit & Loss Extraction
def extract_profit_loss_data(text):
    extracted_data = {
        "Revenue From Operations": extract_value(r"Revenue From Operations[\s\S]*?(\d{1,3}(?:,\d{3})*)", text),
        "Total Income": extract_value(r"Total Income \(I \+ II\)[\s\S]*?(\d{1,3}(?:,\d{3})*)", text),
        "Total Expenses": extract_value(r"Total expenses \(IV\)[\s\S]*?(\d{1,3}(?:,\d{3})*)", text),
    }
    return extracted_data

# ✅ Cash Flow Extraction
def extract_cash_flow_data(text):
    extracted_data = {
        "Net Cash from Operating": extract_value(r"Net Cash Flow generated from/\(used in\) Operating Activities.*?([\d,]+)", text),
        "Net Cash from Investing": extract_value(r"Net Cash Flow used in Investing Activities.*?([\d,]+)", text),
        "Net Cash from Financing": extract_value(r"Net Cash Flow generated from Financing Activities.*?([\d,]+)", text),
    }
    return extracted_data

# ✅ Invoice Extraction (With CGST, SGST, and Total Tax Handling)
def extract_invoice_data(text):
    invoice_number = extract_match(r"Invoice Number\s*:\s*([A-Z0-9-]+)", text)

    # Ensure invoice_number is always a string
    invoice_number = str(invoice_number) if invoice_number else "N/A"

    # ✅ Extract all TOTAL values (Tax Amount & Final Invoice Amount)
    total_matches = re.findall(r"TOTAL:\s*₹([\d,]+\.\d{2})", text)

    if len(total_matches) >= 2:
        tax_amount = float(total_matches[0].replace(",", ""))  # First value → Tax
        total_amount = float(total_matches[1].replace(",", ""))  # Second value → Total Invoice
    else:
        tax_amount = 0
        total_amount = float(total_matches[0].replace(",", "")) if total_matches else 0

    # ✅ Extract CGST & SGST (They are always equal halves of tax amount)
    cgst_match = re.search(r"CGST\s*₹([\d,]+\.\d{2})", text)
    sgst_match = re.search(r"SGST\s*₹([\d,]+\.\d{2})", text)

    if cgst_match and sgst_match:
        cgst = float(cgst_match.group(1).replace(",", ""))
        sgst = float(sgst_match.group(1).replace(",", ""))
        total_tax_amount = cgst + sgst
    else:
        cgst = tax_amount / 2  # If not explicitly found, assume tax is split equally
        sgst = tax_amount / 2
        total_tax_amount = tax_amount

    extracted_data = {
        "Invoice Number": invoice_number,
        "CGST": round(cgst, 2),
        "SGST": round(sgst, 2),
        "Total Tax Amount": round(total_tax_amount, 2),
        "Total Amount": round(total_amount*6, 2)
    }

    return extracted_data

# ✅ Visualization Functions
def visualize_invoice_data(data):
    numeric_data = {k: v for k, v in data.items() if isinstance(v, (int, float))}
    plot_bar_chart(numeric_data, "Invoice Breakdown", "Amount (INR)")

def visualize_balance_sheet(data):
    plot_bar_chart(data, "Balance Sheet Summary", "Amount (INR)")

def visualize_profit_loss(data):
    plot_bar_chart(data, "Profit & Loss Summary", "Amount (INR)")

def visualize_cash_flow(data):
    plot_bar_chart(data, "Cash Flow Summary", "Amount (INR)")


# ✅ Helper Functions
def extract_match(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else "N/A"

def extract_value(pattern, text):
    match = re.search(pattern, text)
    return float(match.group(1).replace(",", "")) if match else 0

def plot_bar_chart(data, title, ylabel):
    if not data:
        st.warning(f"⚠️ No numeric data available for {title}.")
        return
    df = pd.DataFrame(list(data.items()), columns=["Category", "Amount"])
    plt.figure(figsize=(8, 4))
    sns.barplot(x="Category", y="Amount", data=df, palette="coolwarm")
    plt.xticks(rotation=45)
    plt.title(title)
    plt.ylabel(ylabel)
    st.pyplot(plt)
