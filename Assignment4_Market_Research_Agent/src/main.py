import os
import time
import random
import pandas as pd
from dotenv import load_dotenv
from groq import Groq


# -----------------------------
# SYNTHETIC DATA GENERATION
# -----------------------------
def create_synthetic_requests():
    industries = ["EV", "Healthcare", "SaaS", "Retail"]
    regions = ["India", "USA", "Europe", "Asia"]
    objectives = [
        "Market entry analysis",
        "Competitor benchmarking",
        "Growth opportunity study",
        "Risk assessment"
    ]

    data = []
    for i in range(12):
        data.append({
            "request_id": f"REQ{i+1:03d}",
            "industry": random.choice(industries),
            "region": random.choice(regions),
            "objective": random.choice(objectives),
            "time_limit": random.choice([1, 2, 3, 5])  # in seconds (simulated)
        })

    return pd.DataFrame(data)


# -----------------------------
# SHARED MEMORY
# -----------------------------
class SharedMemory:
    def __init__(self):
        self.store = {}

    def write(self, key, value):
        self.store[key] = value

    def read(self, key):
        return self.store.get(key, None)


# -----------------------------
# RATE LIMITER
# -----------------------------
class RateLimiter:
    def __init__(self, max_calls=5, window_sec=10):
        self.max_calls = max_calls
        self.window_sec = window_sec
        self.calls = []

    def wait_if_needed(self):
        now = time.time()

        # remove old calls
        self.calls = [c for c in self.calls if now - c < self.window_sec]

        if len(self.calls) >= self.max_calls:
            sleep_time = self.window_sec - (now - self.calls[0])
            time.sleep(max(0, sleep_time))

        self.calls.append(time.time())


# -----------------------------
# BASE AGENT
# -----------------------------
class BaseAgent:
    def __init__(self, client, memory, limiter):
        self.client = client
        self.memory = memory
        self.limiter = limiter

    def call_llm(self, prompt):
        self.limiter.wait_if_needed()

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a careful business analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"Fallback response due to error: {str(e)}"


# -----------------------------
# SPECIALIST AGENTS
# -----------------------------
class ResearchAgent(BaseAgent):
    def run(self, row):
        prompt = f"""
        Gather key market facts.

        Industry: {row['industry']}
        Region: {row['region']}
        Objective: {row['objective']}

        Provide:
        - Market trends
        - Key players
        - Demand drivers

        If uncertain, say "insufficient data".
        """
        return self.call_llm(prompt)


class SummaryAgent(BaseAgent):
    def run(self, research_text):
        prompt = f"""
        Summarize the following research:

        {research_text}

        Output:
        - 5 bullet summary
        - Clear business insight
        """
        return self.call_llm(prompt)


class RiskAgent(BaseAgent):
    def run(self, research_text):
        prompt = f"""
        Analyze risks from this market research:

        {research_text}

        Output:
        - Top 3 risks
        - Severity (Low/Medium/High)
        - Mitigation strategy
        """
        return self.call_llm(prompt)


# -----------------------------
# ORCHESTRATOR
# -----------------------------
class Orchestrator:
    def __init__(self, client):
        self.memory = SharedMemory()
        self.limiter = RateLimiter(max_calls=6, window_sec=10)

        self.research_agent = ResearchAgent(client, self.memory, self.limiter)
        self.summary_agent = SummaryAgent(client, self.memory, self.limiter)
        self.risk_agent = RiskAgent(client, self.memory, self.limiter)

    def process_request(self, row):

        # Step 1: Research
        research = self.research_agent.run(row)
        self.memory.write(row["request_id"] + "_research", research)

        # Step 2: Summary
        summary = self.summary_agent.run(research)
        self.memory.write(row["request_id"] + "_summary", summary)

        # Step 3: Risk analysis
        risk = self.risk_agent.run(research)
        self.memory.write(row["request_id"] + "_risk", risk)

        # Step 4: Final combined output
        final_report = {
            "request_id": row["request_id"],
            "industry": row["industry"],
            "region": row["region"],
            "objective": row["objective"],
            "research": research,
            "summary": summary,
            "risk_analysis": risk
        }

        return final_report


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("Missing GROQ API Key")

    client = Groq(api_key=api_key)

    # Step 1: dataset
    df = create_synthetic_requests()
    print("Synthetic dataset created")
    
    df.to_csv("research_requests_df.csv", index=False)
    print("Dataset saved as research_requests_df.csv")

    orchestrator = Orchestrator(client)

    results = []

    # Step 2: process each request
    for _, row in df.iterrows():
        print(f"Processing {row['request_id']} ...")
        result = orchestrator.process_request(row)
        results.append(result)

    # Step 3: save output
    output_df = pd.DataFrame(results)
    output_df.to_csv("market_research_reports.csv", index=False)

    print("\nDONE ✔ Reports saved to market_research_reports.csv")


if __name__ == "__main__":
    main()