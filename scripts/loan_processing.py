import numpy as np

# Loan Schemes (Loan Name: [Min Loan, Max Loan])
LOAN_SCHEMES = {
    "SBI Student Loan Scheme": [0, 10],
    "SBI Global Ed-Vantage Scheme": [20, 150],
    "HDFC Bank Education Loan": [0, 20],
    "ICICI Bank Education Loan": [0, 100],
    "Axis Bank Education Loan": [0.5, 75],
    "PNB Udaan": [0, 20],
    "Bank of Baroda Baroda Gyan": [0, 10],
    "Bank of Baroda Baroda Scholar": [0, 20],
    "Canara Bank Vidya Turant": [0, 40],
    "Union Bank of India Education Loan": [0, 30],
    "IDBI Bank Education Loan": [0, 20],
    "Kotak Mahindra Bank Education Loan": [0, 20],
    "Federal Bank Special Vidya Loan": [0, 20],
    "Indian Overseas Bank Vidya Jyoti": [0, 30],
    "UCO Bank Education Loan": [0, 20],
    "Dena Bank Vidya Lakshmi": [0, 15],
    "HSBC India Education Loan": [0, 100],
    "Standard Chartered Bank Education Loan": [0, 150],
    "IDFC FIRST Bank Education Loan": [0, 20],
    "RBL Bank Education Loan": [0, 10],
    "IndusInd Bank Education Loan": [0, 15],
    "Avanse Education Loan": [0.5, 500],
    "InCred Education Loan": [0, 100],
    "Auxilo Finserve Education Loan": [0, 100],
    "MPOWER Financing Education Loan": [0, 100]
}

def calculate_loan_amount(marks_10th, marks_12th, cgpa, total_assets, fixed_deposits):
    """
    Calculates the loan amount based on CGPA, assets, and deposits.
    """
    base_amount = 5  # Base loan amount in lakhs

    # CGPA Boost
    if cgpa >= 9:
        base_amount += 10
    elif cgpa >= 8:
        base_amount += 7
    elif cgpa >= 7:
        base_amount += 4

    # Financial Strength Boost
     if total_assets > 2000000:
        base_amount += 10
    if fixed_deposits > 1000000:
        base_amount += 5

    return min(base_amount, 100)  # Max cap at 100 lakh (1 crore)

def find_suitable_loan(loan_amount):
    """
    Finds the best loan scheme based on the approved loan amount.
    """
    suitable_loans = [loan for loan, (min_amt, max_amt) in LOAN_SCHEMES.items() if min_amt <= loan_amount <= max_amt]
    return suitable_loans if suitable_loans else ["No suitable loan found"]

def predict_loan_eligibility(model, input_data):
    """
    Predicts loan eligibility and suggests a loan scheme if approved.
    
    Args:
        model: Trained RandomForest model
        input_data: List containing 8 selected features

    Returns:
        dict: {Approval Status, Approved Amount, Recommended Loan}
    """
    input_array = np.array(input_data).reshape(1, -1)  # Convert to 2D array
    prediction = model.predict(input_array)[0]

    if prediction == 1:
        # Extract only relevant features for loan amount calculation
        approved_amount = calculate_loan_amount(input_data[0], input_data[1], input_data[2], input_data[5], input_data[6])
        recommended_loans = find_suitable_loan(approved_amount)
        return {"status": "Approved", "amount": approved_amount, "loans": recommended_loans}
    else:
        return {"status": "Rejected", "amount": 0, "loans": ["No loan available"]}
