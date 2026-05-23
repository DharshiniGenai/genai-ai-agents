import pandas as pd
import numpy as np
import random
from groq import Groq
from dotenv import load_dotenv
import os

# =========================
# LOAD API
# =========================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# 1. GENERATE DATASET
# =========================
def generate_data(n=1000):
    data = []

    for i in range(n):
        income = random.randint(20000, 150000)

        rent = random.randint(3000, int(income * 0.3))
        groceries = random.randint(2000, int(income * 0.15))
        transport = random.randint(1000, int(income * 0.1))
        shopping = random.randint(500, int(income * 0.2))
        utilities = random.randint(1000, int(income * 0.1))
        emi = random.randint(0, int(income * 0.4))
        savings_goal = random.randint(5000, int(income * 0.5))

        data.append([
            f"USER_{i+1}",
            income,
            rent,
            groceries,
            transport,
            shopping,
            utilities,
            emi,
            savings_goal
        ])

    df = pd.DataFrame(data, columns=[
        "user_id", "income", "rent", "groceries",
        "transport", "shopping", "utilities", "emi",
        "savings_goal"
    ])

    return df


# =========================
# 2. CLEAN DATA
# =========================
def clean_data(df):
    df = df.dropna()

    numeric_cols = df.columns[1:]
    for col in numeric_cols:
        df = df[df[col] >= 0]

    return df


# =========================
# 3. FEATURE ENGINEERING
# =========================
def feature_engineering(df):
    df["total_spend"] = (
        df["rent"] +
        df["groceries"] +
        df["transport"] +
        df["shopping"] +
        df["utilities"] +
        df["emi"]
    )

    df["savings"] = df["income"] - df["total_spend"]

    df["savings_rate"] = df["savings"] / df["income"]

    df["expense_ratio"] = df["total_spend"] / df["income"]

    return df


# =========================
# 4. RISK DETECTION
# =========================
def risk_analysis(row):
    risks = []

    if row["savings_rate"] < 0.1:
        risks.append("LOW_SAVINGS")

    if row["emi"] / row["income"] > 0.4:
        risks.append("HIGH_EMI")

    if row["total_spend"] > row["income"]:
        risks.append("OVERSPENDING")

    return ", ".join(risks) if risks else "STABLE"


# =========================
# 5. GROQ AI ADVISOR (SAFE)
# =========================
def ai_advice(row):
    prompt = f"""
    You are a financial advisor.

    User Data:
    Income: {row['income']}
    Total Spend: {row['total_spend']}
    Savings Rate: {row['savings_rate']:.2f}
    EMI: {row['emi']}
    Risk: {row['risk']}

    Give:
    1. 3 savings improvement tips
    2. Risk explanation
    3. Budget strategy
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except:
        return "Fallback: Reduce expenses, increase savings to at least 20%, and control EMI load."


# =========================
# 6. MAIN PIPELINE
# =========================
def main():
    print("Generating dataset...")
    df = generate_data(1000)

    print("Cleaning data...")
    df = clean_data(df)

    print("Feature engineering...")
    df = feature_engineering(df)

    print("Running AI agent...")

    advice_list = []

    for i, row in df.iterrows():

        row["risk"] = risk_analysis(row)

        # Use AI only for first 50 users (avoid quota issues)
        if i < 50:
            advice = ai_advice(row)
        else:
            advice = "Rule-based advice: Maintain 20% savings and reduce unnecessary spending."

        advice_list.append(advice)

        print(f"Processed {row['user_id']}")

    df["ai_advice"] = advice_list

    print("Saving output...")
    df.to_csv("financial_advice_output.csv", index=False)

    # Report
    with open("report.txt", "w") as f:
        f.write("""
FINANCIAL AI AGENT REPORT

The system generates synthetic financial data for users and analyzes:
- income vs expenses
- savings rate
- EMI burden

It detects financial risks:
- Overspending
- Low savings
- High EMI load

The AI (Groq LLM) provides personalized financial advice for a subset of users.
For large-scale processing, fallback rule-based logic is used to avoid API overload.

This ensures scalability, cost efficiency, and reliability.
        """)

    print("DONE: CSV + REPORT GENERATED")


if __name__ == "__main__":
    main()