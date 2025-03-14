import pandas as pd
import pdfplumber
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter

def convert_pdf_to_csv(pdf_file):
    """
    Extracts only Date, Transaction Type (Credit/Debit), Amount, and Narration from the bank statement.
    Args:
        pdf_file: Uploaded PDF file
    Returns:
        csv_path: Path of the saved CSV file
    """
    output_csv = "processed_data/bank_statement.csv"
    os.makedirs("processed_data", exist_ok=True)  # Ensure directory exists

    transactions = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    match = re.search(r"(\d{2}-\d{2}-\d{4})\s+(.*?)\s+(\d{1,3}(?:,\d{3})*\.\d{2})\((Dr|Cr)\)", line)
                    if match:
                        date, narration, amount, transaction_type = match.groups()
                        try:
                            amount = float(amount.replace(',', ''))
                            transaction_type = "Credit" if transaction_type == "Cr" else "Debit"
                            transactions.append([date, narration.strip(), transaction_type, amount])
                        except ValueError:
                            continue  # Skip invalid transactions

    # Convert to DataFrame
    if transactions:
        df = pd.DataFrame(transactions, columns=["Date", "Narration", "Transaction Type", "Amount"])
        df.to_csv(output_csv, index=False)
        return output_csv
    else:
        raise ValueError("No valid transactions found in the PDF.")

def extract_transaction_names(df):
    """
    Extracts merchant/person names from UPI or other transactions in the narration.
    Ensures the extracted name list matches the DataFrame length.
    """
    extracted_names = []
    
    for narration in df["Narration"]:
        match = re.search(r"UPI/([^/]*)/", narration)  # Extract name after UPI/
        if match:
            extracted_names.append(match.group(1))
        else:
            match = re.search(r"([A-Z\s]{4,})", narration)  # Extract capitalized merchant names
            if match:
                extracted_names.append(match.group(1).strip())
            else:
                extracted_names.append("Unknown")  # Fill missing values to match DataFrame length

    # Ensure extracted names match DataFrame length
    if len(extracted_names) != len(df):
        extracted_names += ["Unknown"] * (len(df) - len(extracted_names))  # Fill remaining with "Unknown"
    
    df["Transaction Name"] = extracted_names
    return df

def analyze_bank_statement(df):
    """
    Analyzes bank statement data and generates insights & visualizations.
    Args:
        df: DataFrame containing transaction data
    Returns:
        str: Summary of analysis with visualizations
    """
    st.subheader("🏦 Bank Statement Analysis")
    df = extract_transaction_names(df)

    # Summary statistics
    total_deposits = df[df["Transaction Type"] == "Credit"]["Amount"].sum()
    total_withdrawals = df[df["Transaction Type"] == "Debit"]["Amount"].sum()
    highest_deposit = df[df["Transaction Type"] == "Credit"]["Amount"].max()
    highest_withdrawal = df[df["Transaction Type"] == "Debit"]["Amount"].max()

    summary = {
        "Total Deposits": total_deposits,
        "Total Withdrawals": total_withdrawals,
        "Highest Deposit": highest_deposit,
        "Highest Withdrawal": highest_withdrawal,
    }
    st.json(summary)

    # Call visualization function
    visualize_bank_data(df)

    return "Analysis Completed!"

def visualize_bank_data(df):
    """
    Generates visualizations for bank statement data.
    """
    st.subheader("📊 Bank Data Visualizations")
    
    # ✅ **Bar Chart - Deposits vs Withdrawals**
    total_deposits = df[df["Transaction Type"] == "Credit"]["Amount"].sum()
    total_withdrawals = df[df["Transaction Type"] == "Debit"]["Amount"].sum()
    
    plt.figure(figsize=(6, 4))
    sns.barplot(x=["Deposits", "Withdrawals"], y=[total_deposits, total_withdrawals], palette="coolwarm")
    plt.title("💰 Total Deposits vs Withdrawals")
    st.pyplot(plt)

    # ✅ **Pie Chart - Transaction Distribution (Percentages in Legend)**
    plt.figure(figsize=(8, 6))
    transaction_counts = df["Transaction Name"].value_counts()
    total_transactions = transaction_counts.sum()
    
    # 🔥 **Use bright colors for better visualization**
    bright_colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FFD700", "#FF69B4", "#ADFF2F", "#FF4500"]

    wedges, texts = plt.pie(
        transaction_counts, 
        startangle=90, 
        colors=bright_colors[:len(transaction_counts)],  # ✅ Pick only needed colors
        wedgeprops={'edgecolor': 'black'}  # ✅ Add borders for better visibility
    )

    # ✅ **Create legend with percentages**
    legend_labels = [f"{name} - {count/total_transactions:.1%}" for name, count in zip(transaction_counts.index, transaction_counts)]
    plt.title("📌 Transaction Type Distribution")
    plt.legend(wedges, legend_labels, loc="upper left", bbox_to_anchor=(1, 0.5), title="Transaction Names")
    st.pyplot(plt)

    # ✅ **Line Chart - Transactions Over Time**
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(subset=["Date"], inplace=True)
    df.sort_values("Date", inplace=True)
    
    plt.figure(figsize=(8, 4))
    sns.lineplot(x="Date", y="Amount", hue="Transaction Type", data=df, marker="o", palette="Set1")
    plt.xticks(rotation=45)
    plt.title("📈 Transactions Over Time")
    st.pyplot(plt)
