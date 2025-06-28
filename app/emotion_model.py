# emotion_model.py
from transformers import pipeline

classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def detect_emotion(text):
    result = classifier(text)
    return result[0]['label'], result[0]['score']
print(detect_emotion("I feel anxious and stressed."))
# Output: ('fear', 0.89)
