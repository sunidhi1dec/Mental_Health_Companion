from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.emotion_model import detect_emotion
from app.gpt_chat import chat_with_gpt
from app.journal_utils import save_journal_entry

app = FastAPI()

# Enable CORS for frontend (e.g., Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Mental Health Companion backend is running!"}

@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return {"error": "Message is required."}

    # Step 1: Detect emotion
    emotion, confidence = detect_emotion(user_message)

    # Step 2: Generate GPT-like response using Hugging Face
    reply = chat_with_gpt(user_message)

    # Step 3: Save the journal entry with detected mood
    save_journal_entry(user_message, emotion)

    return {
        "reply": reply,
        "emotion": emotion,
        "confidence": confidence
    }
@app.get("/journal/")
async def get_journal_entries():    
    from app.journal_utils import load_journal_entries
    entries = load_journal_entries()
    return entries.to_dict(orient="records")