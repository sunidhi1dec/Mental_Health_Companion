import pandas as pd
from datetime import datetime
import os

def save_journal_entry(text: str, mood: str):
    os.makedirs("data", exist_ok=True)
    entry = {"timestamp": datetime.now(), "text": text, "mood": mood}
    df = pd.DataFrame([entry])
    df.to_csv("data/journal.csv", mode='a', header=not os.path.exists("data/journal.csv"), index=False)
def load_journal_entries():
    if not os.path.exists("data/journal.csv"):
        return pd.DataFrame(columns=["timestamp", "text", "mood"])
    return pd.read_csv("data/journal.csv")