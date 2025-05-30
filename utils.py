import pandas as pd

def check_loan_eligibility(params):
    try:
        df = pd.read_excel("loan_logic.xlsx")
        age = int(params.get("age", 0))
        income = float(params.get("monthly_income", 0))
        credit_score = int(params.get("credit_score", 0))

        for _, row in df.iterrows():
            if row["min_age"] <= age <= row["max_age"] and                income >= row["min_income"] and                credit_score >= row["min_credit_score"]:
                return f"You are eligible for {row['loan_product']} at {row['interest_rate']}% interest."
        return "Sorry, you are not eligible for any loan products at the moment."
    except Exception as e:
        return f"Error processing request: {e}"
