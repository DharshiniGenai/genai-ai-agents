AI Candidate Screening Agent 🧑‍💻📊

An intelligent AI-powered recruitment screening system that evaluates candidates based on skills, experience, and project data, and ranks them using a scoring engine with AI-generated explanations using Groq LLM.

📖 Project Overview

The AI Candidate Screening Agent is a Python-based intelligent recruitment system designed to automate the process of shortlisting candidates for technical job roles.

It generates synthetic candidate profiles, evaluates them using a rule-based scoring engine, and classifies them into different fit levels such as Low, Medium, and High.

To enhance transparency, the system uses Groq’s LLaMA 3.1 model to explain the scoring logic and validate the system behavior like a senior HR AI auditor.

This project demonstrates how Artificial Intelligence can be combined with traditional scoring systems to build explainable and scalable recruitment automation tools.

✨ Features

The system provides a complete AI-driven hiring pipeline including:

Synthetic candidate dataset generation (1000 profiles)
Data cleaning and normalization
Skill-based scoring engine
Experience and project evaluation system
Certification-based scoring boost
Candidate classification (Low / Medium / High)
AI-powered explanation engine using Groq LLM
Transparent scoring logic for HR decision support

The system evaluates candidates based on:

Primary skills match
Secondary skills match
Work experience
Certifications
Project count

🧠 Technologies Used

This project is built using Python and Generative AI.

Main Technologies:

Python
Groq LLM API
LLaMA 3.1 (8B Instant Model)
Pandas
Python Dotenv
Random module

⚙️ How the Project Works

The system starts by generating synthetic candidate profiles including skills, experience, certifications, and project counts.

Next, the data is cleaned and normalized to ensure consistency in text fields such as skills and domain names.

After preprocessing, each candidate is evaluated using a scoring engine that assigns points based on experience, skill matching, certifications, and project experience.

Candidates are then classified into three categories:

Low Fit
Medium Fit
High Fit

Finally, Groq LLM is used to analyze the scoring logic and generate a detailed explanation of how the system works.

📊 Scoring System Breakdown

The scoring engine evaluates candidates based on:

Factor	Weight
Experience	30 points
Primary Skill Match	25 points
Secondary Skills	20 points
Certifications	10 points
Projects	15 points

Final score is normalized between 0 and 100.

## 📂 Project Structure

```
Assignment3_Candidate_Screening/
│
├── output/
│   ├── candidate_screening_results.csv
│   └── terminal_output.txt
│
├── src/
│   ├── .env
│   └── main.py
│
├── README.md
└── requirements.txt
```

🧠 Job Role Configuration

The system is designed for a sample job role:

Domain: Data Science
Required Skills: Python, ML, SQL
Preferred Skills: DL, AWS, Docker
Minimum Experience: 2 years
Minimum Projects: 3

📦 Installation

Install required dependencies:

pip install pandas groq python-dotenv

🔑 API Key Setup

To use Groq LLM:

Create an account on Groq
Generate API key
Create a .env file
GROQ_API_KEY=your_api_key_here

▶️ Running the Project

Run the system using:

python main.py

The system will:

Generate candidate dataset
Clean and process data
Score each candidate
Classify fit level
Generate AI explanation
Save results in CSV

📁 Output Files

After execution, the system generates:

candidate_screening_results.csv → Final ranked candidate dataset
AI explanation output → Printed in terminal (Groq LLM analysis)

🧩 Key Design Decisions

Synthetic dataset ensures safe and scalable testing
Rule-based scoring ensures consistency and transparency
AI explanation layer improves interpretability
Weighted scoring system simulates real HR evaluation
Hybrid AI + rule-based design ensures reliability
Normalization ensures fair comparison across candidates

🚨 Error Handling

The system includes safety mechanisms:

Handles missing or invalid candidate data
Prevents score overflow using normalization
Ensures fallback explanation if AI fails
Avoids crashes during API errors
Graceful handling of empty fields

📈 Learning Outcomes

This project helps in understanding:

Recruitment automation systems
Rule-based scoring engines
Feature weighting techniques
Data preprocessing and normalization
AI explainability using LLMs
HR tech and candidate evaluation systems
Hybrid AI system design

🔮 Future Improvements

This system can be enhanced further with:

Resume parsing using NLP
Real job portal integration
Interview question generation
Skill graph matching system
Bias detection in hiring
Web dashboard (React / Streamlit)
Database storage for candidates
Real-time job matching system

👨‍💻 Conclusion

The AI Candidate Screening Agent demonstrates how Artificial Intelligence can be used to automate recruitment while maintaining transparency and fairness.

By combining a structured scoring engine with Groq LLM-based explanations, the system ensures both accuracy and interpretability in candidate evaluation.

It is a strong example of how AI can modernize HR processes and support smarter hiring decisions.