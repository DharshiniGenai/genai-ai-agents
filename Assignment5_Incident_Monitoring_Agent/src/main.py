import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from groq import Groq


def generate_logs(days=20, services=None):
    if services is None:
        services = ["auth", "payments", "search", "recommendation"]

    start_time = datetime.now() - timedelta(days=days)
    records = []

    for i in range(days * 24 * 6):  # 10-min intervals
        timestamp = start_time + timedelta(minutes=10 * i)

        for service in services:
            cpu = random.uniform(20, 70)
            memory = random.uniform(30, 70)
            latency = random.uniform(50, 200)
            error_rate = random.uniform(0.0, 0.02)
            incident_flag = 0

            # Inject anomalies
            if random.random() < 0.02:
                latency *= random.uniform(3, 8)
                error_rate += random.uniform(0.1, 0.3)
                memory += random.uniform(20, 50)
                incident_flag = 1

            records.append([
                timestamp, service, cpu, memory, latency, error_rate, incident_flag
            ])

    df = pd.DataFrame(records, columns=[
        "timestamp", "service_name", "cpu_usage",
        "memory_usage", "latency_ms", "error_rate", "incident_flag"
    ])

    return df


def feature_engineering(df):
    df = df.sort_values("timestamp")

    df["rolling_mean_latency"] = df.groupby("service_name")["latency_ms"] \
        .transform(lambda x: x.rolling(6, min_periods=1).mean())

    df["error_rate_trend"] = df.groupby("service_name")["error_rate"] \
        .transform(lambda x: x.diff().fillna(0))

    # Simple anomaly score (normalized heuristic)
    df["anomaly_score"] = (
        (df["latency_ms"] / 1000) +
        df["error_rate"] * 10 +
        (df["memory_usage"] / 100)
    )

    return df


def detect_incidents(df):
    incidents = []

    for _, row in df.iterrows():
        severity = "LOW"
        action = "Monitor"

        if row["anomaly_score"] > 3:
            severity = "HIGH"
            action = "Scale up + restart service"
        elif row["anomaly_score"] > 2:
            severity = "MEDIUM"
            action = "Investigate latency + check logs"

        escalation = severity == "HIGH"

        incidents.append({
            "timestamp": row["timestamp"],
            "service": row["service_name"],
            "anomaly_score": row["anomaly_score"],
            "severity": severity,
            "action": action,
            "escalate_to_human": escalation
        })

    return pd.DataFrame(incidents)


def groq_summary(client, incident_df):
    sample = incident_df.head(30).to_string()

    prompt = f"""
You are an AI Operations engineer.

Analyze these incidents and produce:
1. Incident summary
2. Root cause possibilities
3. Recommended actions
4. Escalation policy
5. Monitoring improvements

Data:
{sample}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior SRE and AI ops expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def main():

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY")

    client = Groq(api_key=api_key)

    # 1. Generate logs
    logs_df = generate_logs(days=20)

    # 2. Clean + sort
    logs_df = logs_df.sort_values("timestamp")

    # 3. Feature engineering
    logs_df = feature_engineering(logs_df)

    # 4. Incident detection
    incident_df = detect_incidents(logs_df)

    # 5. Save results
    incident_df.to_csv("incident_analysis_results.csv", index=False)

    # 6. AI summary report
    summary = groq_summary(client, incident_df)

    with open("incident_response_strategy_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("\nDONE ✔")
    print("Files generated:")
    print("- incident_analysis_results.csv")
    print("- incident_response_strategy_summary.txt")


if __name__ == "__main__":
    main()