import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load synthetic dataset
df = pd.read_csv("data/loan_approval_data.csv")

# Print actual column names to verify
print("Dataset Columns:", df.columns)

# Define the selected features
selected_features = [
    "Marks_10th",
    "Marks_12th",
    "CGPA",
    "Parents_Credit_Score",
    "Student_Credit_Score",
    "Total_Assets",
    "Fixed_Deposit",
    "Selected_Exam_Rank"
]

# Create 'Selected_Exam_Rank' dynamically (selects one of the 4 exam ranks)
df["Selected_Exam_Rank"] = df[["JEE_Rank", "SAT_Score", "CAT_Rank", "NEET_Rank"]].max(axis=1)

# Select only required features + target column
df = df[selected_features + ["Loan_Approved"]]

# Split dataset
X = df[selected_features]
y = df["Loan_Approved"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model
pickle.dump(model, open("models/loan_approval_model.pkl", "wb"))

print("✅ Model trained and saved successfully!")
