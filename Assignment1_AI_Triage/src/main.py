import os
import random
import re
import time
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from google import genai


# =========================================
# 1. SYNTHETIC DATA GENERATION
# =========================================

def generate_messages(n=1500):

    billing = [
        "I was charged twice for my order",
        "Refund not received yet",
        "Payment failed but money deducted",
        "Need invoice for my purchase",
        "Coupon code not working"
    ]

    delivery = [
        "My package has not arrived",
        "Delivery delayed again",
        "Wrong item delivered",
        "Tracking not updating",
        "Order stuck in transit"
    ]

    technical = [
        "App is crashing",
        "Cannot login to account",
        "Website not loading",
        "Error during payment",
        "Password reset not working"
    ]

    complaint = [
        "Very bad service",
        "I am unhappy with support",
        "No response from team",
        "Worst experience ever",
        "I want refund immediately"
    ]

    channels = ["Email", "Chat", "App", "Social"]

    data = []

    for i in range(n):

        category = random.choice(["billing", "delivery", "technical", "complaint"])

        if category == "billing":
            msg = random.choice(billing)
        elif category == "delivery":
            msg = random.choice(delivery)
        elif category == "technical":
            msg = random.choice(technical)
        else:
            msg = random.choice(complaint)

        if random.random() < 0.2:
            msg += " !!! urgent help !!!"

        if random.random() < 0.05:
            msg = "   "

        data.append({
            "message_id": f"MSG{i:05d}",
            "customer_id": f"CUST{random.randint(1000,9999)}",
            "timestamp": datetime.now() - timedelta(days=random.randint(0, 30)),
            "message_text": msg,
            "channel": random.choice(channels),
            "previous_tickets": random.randint(0, 5)
        })

    return pd.DataFrame(data)


# =========================================
# 2. TEXT CLEANING
# =========================================

def clean_text(text):

    if not text or text.strip() == "":
        return "empty message"

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================================
# 3. GEMINI CLASSIFIER (FIXED MODEL)
# =========================================

def gemini_classify(client, message):

    prompt = f"""
You are a customer support AI agent.

Return STRICT format:

Intent: Billing | Delivery | Technical | Complaint | Fraud | Legal | Unknown
Priority: Low | Medium | High | Critical
Escalation: Yes or No
Suggested Reply: short helpful response

Message:
{message}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Gemini error:", e)
        return None


# =========================================
# 4. FALLBACK RULE SYSTEM
# =========================================

def fallback_rule(message):

    msg = message.lower()

    if any(x in msg for x in ["fraud", "hacked", "legal", "court"]):
        return {
            "intent": "Fraud",
            "priority": "Critical",
            "escalation_flag": "Yes",
            "suggested_reply": "We are escalating your issue immediately."
        }

    if any(x in msg for x in ["refund", "payment", "charged", "invoice"]):
        return {
            "intent": "Billing",
            "priority": "Medium",
            "escalation_flag": "No",
            "suggested_reply": "We are checking your billing issue."
        }

    if any(x in msg for x in ["delivery", "package", "tracking"]):
        return {
            "intent": "Delivery",
            "priority": "Medium",
            "escalation_flag": "No",
            "suggested_reply": "We are checking your order status."
        }

    if any(x in msg for x in ["crash", "error", "login", "password"]):
        return {
            "intent": "Technical",
            "priority": "Medium",
            "escalation_flag": "No",
            "suggested_reply": "We are working on your technical issue."
        }

    if any(x in msg for x in ["bad", "worst", "unhappy"]):
        return {
            "intent": "Complaint",
            "priority": "High",
            "escalation_flag": "Yes",
            "suggested_reply": "We are sorry for your experience."
        }

    return {
        "intent": "Unknown",
        "priority": "Low",
        "escalation_flag": "No",
        "suggested_reply": "We will assist you shortly."
    }


# =========================================
# 5. PARSE GEMINI OUTPUT
# =========================================

def parse_output(text):

    result = {
        "intent": "Unknown",
        "priority": "Low",
        "escalation_flag": "No",
        "suggested_reply": "We will assist you shortly."
    }

    if not text:
        return result

    try:
        for line in text.split("\n"):

            line = line.strip().lower()

            if line.startswith("intent:"):
                result["intent"] = line.split(":", 1)[1].strip()

            elif line.startswith("priority:"):
                result["priority"] = line.split(":", 1)[1].strip()

            elif line.startswith("escalation:"):
                result["escalation_flag"] = line.split(":", 1)[1].strip()

            elif line.startswith("suggested reply:"):
                result["suggested_reply"] = line.split(":", 1)[1].strip()

    except:
        pass

    return result


# =========================================
# 6. MAIN FUNCTION
# =========================================

def main():

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    print("\nAI TRIAGE AGENT STARTED\n")

    # STEP 1: DATA
    df = generate_messages(1200)
    df.to_csv("synthetic_messages.csv", index=False)

    df["cleaned"] = df["message_text"].apply(clean_text)

    results = []

    # =========================================
    # AI LIMIT CONTROL
    # =========================================

    ai_call_count = 0
    AI_LIMIT = 20

    # =========================================
    # PROCESS LOOP
    # =========================================

    for i, row in df.iterrows():

        msg = row["cleaned"]

        print("Processing:", row["message_id"])

        # AI ONLY FOR FIRST 20 CALLS
        if ai_call_count < AI_LIMIT:

            response = gemini_classify(client, msg)

            if response:
                parsed = parse_output(response)
            else:
                parsed = fallback_rule(msg)

            ai_call_count += 1

        # AFTER LIMIT → FALLBACK ONLY
        else:
            parsed = fallback_rule(msg)

        # SAFETY CHECK
        if not isinstance(parsed, dict):
            parsed = fallback_rule(msg)

        results.append({
            "message_id": row["message_id"],
            "customer_id": row["customer_id"],
            "message_text": row["message_text"],
            "intent": parsed["intent"],
            "priority": parsed["priority"],
            "suggested_reply": parsed["suggested_reply"],
            "escalation_flag": parsed["escalation_flag"]
        })

    # SAVE OUTPUT
    out_df = pd.DataFrame(results)
    out_df.to_csv("triage_results.csv", index=False)

    # SUMMARY
    with open("summary.txt", "w") as f:
        f.write("""
AI CUSTOMER SUPPORT TRIAGE AGENT

✔ Synthetic dataset generation (1200 messages)
✔ Gemini AI used for first 20 calls only
✔ Rule-based fallback for remaining messages
✔ Handles billing, delivery, technical, complaints
✔ Fraud & legal escalation detection
✔ Quota-safe hybrid architecture
✔ Produces structured CSV output
""")

    print("\nDONE: Files generated successfully")
    print("synthetic_messages.csv")
    print("triage_results.csv")
    print("summary.txt")


# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    main()