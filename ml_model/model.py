from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Initialize the FastAPI app
app = FastAPI()


# Pydantic schema for input validation
class SentimentRequest(BaseModel):
    text: str


# Global pipeline instance
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1)  # Ensure CPU usage


# Function to run the actual sentiment model
def run_sentiment_model(text: str) -> float:
    sentiment = sentiment_pipeline([text])[0]
    label = sentiment['label']
    score = sentiment['score'] if label == 'POSITIVE' else -sentiment['score']
    return score


# Endpoint for sentiment analysis
@app.post("/analyse/")
def analyse_sentiment(request: SentimentRequest):
    text = request.text
    # sentiment = min((len(text)-10)/10, 1)
    sentiment = run_sentiment_model(text)
    thresholds = [(-0.5, 'very negative'),
                  (-0.2, 'somewhat negative'),
                  (0.2, 'neutral'),
                  (0.5, 'somewhat positive'),
                  (1.0, 'very positive')]

    for threshold, label in thresholds:
        if sentiment <= threshold:
            return {"sentiment": sentiment, 'label': label}
    raise ValueError('Sentiment could not be calculated')
