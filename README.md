DEPLOYMENT web app deployed link:https://shivaravula18-bfsi-ocr-loan-prediction-app-dyfjak.streamlit.app/
BFSI OCR Loan Prediction System 🚀
An advanced OCR-based loan prediction system for the BFSI sector, integrating text extraction, multi-language OCR, document analysis, financial data processing, and loan eligibility prediction.

🔹 Features
✅ OCR Extraction: Extracts text from images, PDFs, and documents using the best OCR techniques.

✅ Multi-Language OCR: Detects & translates text dynamically from any global or Indian language to English.

✅ Bank Statement Analysis: Reads bank statements, categorizes expenses, and provides visual insights.

✅ Loan Prediction System: Uses financial data & AI to determine loan eligibility & suggest best options.

✅ Stock Market Analysis: Compares two stocks dynamically using live financial data.

✅ Invoice Processing: Extracts CGST, SGST, Total Tax & Final Amount from invoices.

✅ CSV Clustering (Unstructured Data): Clusters numeric data and provides visual insights.

✅ Google OAuth Login: Users can securely log in using Google authentication.



🔹 Installation
1️⃣ Clone the Repository
bash
git clone https://github.com/Shivaravula18/BFSI_OCR_LOAN_PREDICTION.git
cd BFSI_OCR_LOAN_PREDICTION

2️⃣ Install Dependencies
bash
pip install -r requirements.txt

3️⃣ Run the Application
bash
streamlit run app.py


🔹 File Structure
bash

📂 BFSI_OCR_LOAN_PREDICTION/
│── 📜 app.py                # Main Streamlit app

│── 📂 scripts/               # All backend processing scripts

│    ├── ocr_preprocess.py    # OCR text extraction

│    ├── multi_lang_ocr.py    # Multi-language OCR

│    ├── expenditure_analysis.py # Bank Statement Analysis

│    ├── document_processing.py  # Structured & Unstructured Document Handling

│    ├── loan_processing.py   # Loan eligibility prediction

│    ├── stock_market_analyzer.py # Stock Market Analysis

│── 📜 requirements.txt       # Project dependencies

│── 📜 styles.css             # CSS for UI design

│── 📜 packages.txt

│── 📜 README.md              # Project documentation


🔹 Technologies Used
Python 🐍
Streamlit 🌐
Tesseract OCR 🔍
OpenCV 📸
Pandas & NumPy 📊
Matplotlib & Seaborn 📈
Scikit-learn 🤖 (For K-Means Clustering & ML)
Google OAuth 🔑
🔹 Deployment
To deploy this on Streamlit Cloud or any server, make sure you have:

A working GitHub repo with requirements.txt
OAuth credentials configured in Google Cloud Console
🔹 Author
👤 Shiva Ravula
📧 [ravula.shivakumar11@gmail.com]

🔹 License
📜 MIT License
Copyright (c) 2024 Vidzai Digital

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
