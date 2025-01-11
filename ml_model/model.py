from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()


# Pydantic schema for input validation
class SentimentRequest(BaseModel):
    text: str


# Endpoint for sentiment analysis
@app.post("/analyse/")
def analyse_sentiment(request: SentimentRequest):
    """
    Mock sentiment analysis endpoint.
    """

    text = request.text
    sentiment = min((len(text)-10)/10, 1)
    thresholds = [(-0.5, 'very negative'),
                  (-0.2, 'somewhat negative'),
                  (0.2, 'neutral'),
                  (0.5, 'somewhat positive'),
                  (1.0, 'very positive')]

    for threshold, label in thresholds:
        if sentiment <= threshold:
            return {"sentiment": sentiment, 'label': label}
    raise ValueError('Sentiment could not be calculated')

