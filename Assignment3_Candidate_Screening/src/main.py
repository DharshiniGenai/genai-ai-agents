import os
import random
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# 1. CONFIG
# -----------------------------
DOMAINS = ["AI", "Web Development", "Data Science", "Cloud", "Cyber Security", "Mobile Dev"]

SKILLS = [
    "python", "java", "react", "node", "sql",
    "ml", "dl", "aws", "docker", "kubernetes",
    "flutter", "android", "cybersecurity"
]

CERTIFICATIONS = [
    "AWS Certified", "Google Cloud Certified",
    "Azure Fundamentals", "TensorFlow Certificate",
    "None"
]


# -----------------------------
# 2. SYNTHETIC DATA GENERATION
# -----------------------------
def generate_candidates(n=1000):
    data = []

    for i in range(n):
        primary = random.choice(SKILLS)
        secondary = random.sample(SKILLS, k=random.randint(1, 4))

        cert = random.choice(CERTIFICATIONS)

        row = {
            "candidate_id": f"CAND_{i+1}",
            "years_experience": round(random.uniform(0, 10), 1),
            "primary_skill": primary,
            "secondary_skills": ",".join(secondary),
            "domain": random.choice(DOMAINS),
            "certifications": cert,
            "projects_count": random.randint(0, 20)
        }

        data.append(row)

    return pd.DataFrame(data)


# -----------------------------
# 3. CLEANING & NORMALIZATION
# -----------------------------
def clean_data(df):
    df["primary_skill"] = df["primary_skill"].str.lower().str.strip()
    df["secondary_skills"] = df["secondary_skills"].str.lower().str.replace(" ", "")
    df["domain"] = df["domain"].str.lower().str.strip()
    df["certifications"] = df["certifications"].fillna("none").str.lower()
    return df


# -----------------------------
# 4. JOB REQUIREMENT CONFIG
# -----------------------------
JOB_ROLE = {
    "domain": "data science",
    "required_primary": ["python", "ml", "sql"],
    "preferred_secondary": ["dl", "aws", "docker"],
    "min_experience": 2,
    "min_projects": 3
}


# -----------------------------
# 5. SCORING ENGINE
# -----------------------------
def score_candidate(row):
    score = 0

    # Experience (30 points)
    exp = row["years_experience"]
    if exp >= JOB_ROLE["min_experience"]:
        score += min(30, exp * 3)
    else:
        score += exp * 10  # partial credit

    # Primary skill match (25 points)
    if row["primary_skill"] in JOB_ROLE["required_primary"]:
        score += 25

    # Secondary skills match (20 points)
    secondary = row["secondary_skills"].split(",")
    match = sum(1 for s in secondary if s in JOB_ROLE["preferred_secondary"])
    score += match * 5

    # Certifications (10 points)
    if row["certifications"] != "none":
        score += 10

    # Projects (15 points)
    score += min(15, row["projects_count"] * 1.5)

    # Fallback penalty for missing/invalid data
    if pd.isna(row["primary_skill"]) or row["primary_skill"] == "":
        score -= 10

    return max(0, min(100, round(score, 2)))


# -----------------------------
# 6. CLASSIFICATION
# -----------------------------
def classify(score):
    if score < 40:
        return "Low"
    elif score < 70:
        return "Medium"
    else:
        return "High"


# -----------------------------
# 7. GROQ AI EXPLANATION AGENT
# -----------------------------
def explain_scoring_with_groq(client, sample_df):
    prompt = f"""
You are a CODE AUDITOR AI.

STRICT RULES:
- Do NOT paraphrase logic
- Do NOT interpret beyond code
- ONLY explain what is explicitly written
- If unsure → say "NOT SPECIFIED IN CODE"
- Do NOT add assumptions

OUTPUT FORMAT:
1. Line-by-line explanation
2. Validation result (Correct / Incorrect)
3. Bugs (ONLY if explicit logical error exists)

CODE:
{open("main.py").read()}

SAMPLE DATA:
{sample_df.head(5).to_string(index=False)}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior HR AI system designer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# 8. MAIN PIPELINE
# -----------------------------
def main():

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ API KEY")

    client = Groq(api_key=api_key)

    print("Generating synthetic dataset...")
    df = generate_candidates(1000)

    print("Cleaning data...")
    df = clean_data(df)

    print("Scoring candidates...")
    df["score"] = df.apply(score_candidate, axis=1)
    df["fit_level"] = df["score"].apply(classify)

    print("Saving results...")
    df.to_csv("candidate_screening_results.csv", index=False)

    print("Generating AI explanation...")
    explanation = explain_scoring_with_groq(client, df)

    print("\n===== AI AGENT EXPLANATION =====\n")
    print(explanation)

    print("\nDONE: candidate_screening_results.csv created")


if __name__ == "__main__":
    main()