import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧠 AI Mental Health Companion", page_icon="💬")
st.title("🧠 AI Mental Health Companion")

st.markdown("This app provides emotional support and tracks your mood over time.")

# Input area for user's journal entry
user_input = st.text_area("📝 Share your thoughts or how you're feeling:", height=150, placeholder="E.g., I'm feeling a bit overwhelmed today...")

# Process input
if st.button("💬 Talk to Companion"):
    if not user_input.strip():
        st.warning("Please enter something first.")
    else:
        with st.spinner("Analyzing and generating response..."):
            try:
                response = requests.post("http://localhost:8000/chat/", json={"message": user_input})
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"**Emotion Detected:** {data['emotion']} (Confidence: {data['confidence']:.2f})")
                    st.markdown("**💬 Companion says:**")
                    st.info(data['reply'])
                else:
                    st.error("Backend error. Make sure FastAPI is running.")
            except Exception as e:
                st.error(f"Error: {e}")

# Display mood trends
if st.button("📊 Show Mood Trends"):
    try:
        df = pd.read_csv("data/journal.csv")

        # Convert the timestamp column to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Drop rows with invalid timestamps
        df = df.dropna(subset=["timestamp"])

        # Extract just the date for grouping
        df["date"] = df["timestamp"].dt.date

        # Group and count moods per day
        mood_counts = df.groupby(["date", "mood"]).size().unstack(fill_value=0)

        st.subheader("📈 Mood Trends Over Time")
        fig, ax = plt.subplots(figsize=(10, 4))
        mood_counts.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    except FileNotFoundError:
        st.warning("No journal entries yet. Talk to the companion first.")

