AI Customer Support Triage Agent 🤖📩

An intelligent AI-powered system that classifies customer support messages, assigns priority levels, detects escalation needs, and generates automated replies using Google Gemini AI with a reliable fallback rule engine.

📖 Project Overview

The AI Customer Support Triage Agent is a Python-based intelligent automation system designed to handle large volumes of customer support messages efficiently.

It generates synthetic customer queries and processes them using a hybrid architecture that combines Google Gemini AI and a rule-based fallback system. The system automatically classifies each message into categories such as Billing, Delivery, Technical, Complaint, Fraud, or Legal, and assigns a priority level along with escalation decisions.

This project demonstrates how AI can be used in real-world customer service systems to reduce human workload, improve response speed, and ensure consistent support quality.

✨ Features

The system provides a complete AI-driven support automation pipeline including:

Synthetic customer message generation (1200 samples)
Automatic text cleaning and preprocessing
AI-based intent classification using Gemini
Rule-based fallback system for reliability
Priority detection (Low / Medium / High / Critical)
Escalation decision (Yes / No)
Automated suggested replies
Hybrid AI + rule-based architecture
API quota-safe execution (limited AI calls)

The system classifies messages into:

Billing
Delivery
Technical
Complaint
Fraud
Legal
Unknown

🧠 Technologies Used

This project is built using Python and Generative AI.

Main Technologies:

Python
Google Gemini AI (gemini-2.5-flash)
Google GenAI SDK
Pandas
Regex (text processing)
Dotenv (environment management)

⚙️ How the Project Works

The system follows a structured pipeline:

First, it generates synthetic customer support messages across multiple categories such as billing issues, delivery delays, technical errors, and complaints.

Next, the messages are cleaned using preprocessing techniques like lowercasing, removing special characters, and trimming extra spaces.

After preprocessing, each message is sent to Google Gemini AI for classification. The AI returns structured outputs including intent, priority, escalation flag, and suggested replies.

To ensure reliability, the system uses a fallback rule engine when:

API quota is exceeded
API fails
After the first 20 AI calls

Finally, all results are stored in a structured CSV file for further analysis.

📥 System Output Structure

Each processed message contains:

Field	Description
message_id	Unique ID of the message
customer_id	Customer identifier
message_text	Original message
intent	Classified category
priority	Assigned urgency level
escalation_flag	Whether human support is required
suggested_reply	Auto-generated response

📊 Output Files

After execution, the system generates:

synthetic_messages.csv → Generated dataset
triage_results.csv → Final classified results
summary.txt → System overview report

## 📂 Project Structure

```
Assignment1_AI_Triage/
│
├── output/
│   ├── summary.txt
│   ├── synthetic_messages.csv
│   └── triage_results.csv
│
├── src/
│   ├── .env
│   └── main.py
│
├── README.md
└── requirements.txt
```

🧠 Key Design Decisions

Hybrid AI + Rule System ensures system never fails completely
AI call limit (20 requests) prevents API quota exhaustion
Rule-based fallback guarantees continuous operation
Clean structured output enables easy integration with real systems
Simple CSV-based storage for analysis and reporting

📦 Installation

Install required dependencies:

pip install pandas python-dotenv google-genai

🔑 API Key Setup

To use Gemini AI:

Get API key from Google AI Studio
Create a .env file
Add:
GEMINI_API_KEY=your_api_key_here

▶️ Running the Project

Run the system using:

python main.py

The system will:

Generate synthetic messages
Process them using AI + rules
Save final results automatically

🚨 Error Handling

The system is designed with strong reliability features:

Handles API failures safely
Prevents crashes using fallback system
Manages empty or invalid messages
Ensures output generation even without AI

🧩 Learning Outcomes

This project helps you understand:

AI-powered classification systems
Prompt engineering with LLMs
Hybrid AI + rule-based architecture
Real-world customer support automation
API integration using Python
Data preprocessing and cleaning
Fault-tolerant system design

🔮 Future Improvements

This system can be improved further by adding:

Real-time dashboard (Streamlit / React)
Database integration (MongoDB / PostgreSQL)
Advanced sentiment analysis layer
Multi-language support
REST API using FastAPI
Live chatbot integration
Ticket tracking system

👨‍💻 Conclusion

The AI Customer Support Triage Agent demonstrates how Artificial Intelligence can be applied to automate customer service workflows efficiently.

By combining Google Gemini AI with a rule-based fallback system, the project ensures both intelligence and reliability in real-world scenarios.

It is a strong example of how AI systems can be designed for scalability, fault tolerance, and practical business use.