AI Financial Advisor Agent 💰📊

An intelligent AI-powered financial analysis system that generates personalized budget insights, detects financial risks, and provides savings recommendations using Groq LLM with a scalable fallback logic system.

📖 Project Overview

The AI Financial Advisor Agent is a Python-based intelligent system designed to analyze user financial data and provide actionable money management advice.

It generates synthetic financial profiles for users, performs feature engineering, detects financial risk patterns, and uses Groq’s LLM (LLaMA 3.1) to generate personalized financial guidance.

The system is designed to simulate real-world financial advisory services, helping users understand spending behavior, savings patterns, and EMI risks in a structured and intelligent way.

✨ Features

The system provides a complete financial intelligence pipeline including:

Synthetic financial dataset generation (1000 users)
Data cleaning and validation
Feature engineering for financial insights
Risk detection system
AI-powered financial advice using Groq LLM
Rule-based fallback advisory system
Scalable processing for large datasets
Automated CSV and report generation

The system analyzes key financial factors:

Income vs Expenses
Savings rate
EMI burden
Spending behavior
Financial stability status

🧠 Technologies Used

This project is built using Python and Generative AI.

Main Technologies:

Python
Groq LLM API
LLaMA 3.1 (8B Instant Model)
Pandas
NumPy
Python Dotenv

⚙️ How the Project Works

The system starts by generating synthetic financial profiles for users, including income, rent, groceries, transport, shopping, utilities, EMI, and savings goals.

Next, the data is cleaned by removing missing or invalid values and ensuring consistency across numerical fields.

Feature engineering is then applied to calculate:

Total spending
Savings amount
Savings rate
Expense ratio

After that, a risk analysis engine evaluates each user and categorizes financial risks such as low savings, high EMI burden, or overspending.

Finally, Groq’s LLM is used to generate personalized financial advice for the first 50 users. For the remaining users, a rule-based fallback system ensures scalability and avoids API overload.

📊 Financial Metrics Generated

The system computes the following key metrics:

Metric	Description
Total Spend	Total monthly expenses
Savings	Income minus expenses
Savings Rate	Percentage of income saved
Expense Ratio	Ratio of expenses to income

⚠️ Risk Detection System

The model identifies financial risks such as:

LOW_SAVINGS → Savings rate below 10%
HIGH_EMI → EMI exceeds 40% of income
OVERSPENDING → Expenses exceed income

If no risks are detected, the user is classified as:

STABLE

## 📂 Project Structure

```
Assignment2_Financial_Agent/
│
├── output/
│   ├── financial_advice_output.csv
│   └── report.txt
│
├── src/
│   ├── .env
│   └── main.py
│
├── README.md
└── requirements.txt
```
📦 Installation

Install required dependencies:

pip install pandas numpy groq python-dotenv

🔑 API Key Setup

To use Groq LLM:

Create an account on Groq
Generate API key
Create a .env file
GROQ_API_KEY=your_api_key_here

▶️ Running the Project

Run the program using:

python main.py

The system will:

Generate financial dataset
Analyze user finances
Detect risks
Generate AI + rule-based advice
Save results into files

📁 Output Files

After execution, the system generates:

financial_advice_output.csv → Full user financial analysis
report.txt → Summary report of system behavior

🧠 Key Design Decisions

Synthetic dataset ensures safe testing without real financial data
Feature engineering improves AI decision quality
Risk detection system provides explainability
AI limited to first 50 users to control API cost
Rule-based fallback ensures system never fails
Hybrid architecture improves scalability and reliability

🚨 Error Handling

The system includes robust safety mechanisms:

Handles API failures gracefully
Uses fallback advice when AI is unavailable
Ensures no negative or invalid financial values
Prevents system crash during large dataset processing

📈 Learning Outcomes

This project helps in understanding:

Financial data analysis using Python
Feature engineering techniques
Risk scoring systems
LLM integration with real-world data
Hybrid AI + rule-based systems
Scalable AI system design
Financial advisory system logic

🔮 Future Improvements

This system can be improved further by adding:

Real-time banking data integration
Personalized investment recommendations
Credit score prediction
Expense tracking dashboard (Streamlit / React)
Multi-month financial forecasting
Tax optimization suggestions
Mobile app integration

👨‍💻 Conclusion

The AI Financial Advisor Agent demonstrates how Artificial Intelligence can be used to analyze financial behavior and provide meaningful money management advice.

By combining Groq LLM with a structured rule-based system, the project ensures both intelligence and reliability in financial decision-making.

It is a strong example of how AI can be applied to real-world financial planning problems in a scalable and practical way.