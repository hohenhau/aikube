import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Initialise the FastAPI app
app = FastAPI()

# Specify the machine learning model URL
ML_MODEL_URL = os.getenv("ML_MODEL_URL")  # Loaded from .env or the docker-compose file


async def analyse_sentiment(text: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{ML_MODEL_URL}/analyse/", json={"text": text})
        response.raise_for_status()
        return response.json()


@app.post("/analyse_text", response_model=schemas.AnalyseAndOrAddText)  # Specifies response validation
async def analyse_text(request: schemas.AnalyseAndOrAddText):  # Specifies request validation
    sentiment = await analyse_sentiment(request.text)  # Use `request.text`
    return {"text": request.text, "sentiment": sentiment["sentiment"]}


# Analyse and add a piece of text to the database
@app.post("/texts/analyse_and_add_text", response_model=schemas.AnalyseAndOrAddText)  # Specifies response validation
async def analyse_and_add_text(request: schemas.AnalyseAndOrAddText, db: Session = Depends(get_db)):
    sentiment = await analyse_sentiment(request.text)  # Call ML model to get sentiment
    # Create new entry with text and sentiment
    db_entry = models.SentimentEntry(text=request.text, sentiment=sentiment['sentiment'])
    db.add(db_entry)
    db.commit()
    return db_entry


# Add a piece of text and its sentiment value (between 0 and 1) to the database
@app.post("/texts/add_text_and_sentiment", response_model=schemas.AnalyseAndOrAddText)  # Specifies response validation
async def add_text_and_sentiment(request: schemas.AnalyseAndOrAddText, db: Session = Depends(get_db)):
    if not (-1 <= request.sentiment <= 1):
        raise HTTPException(status_code=400, detail="Sentiment value must be between -1 and 1")
    db_entry = models.SentimentEntry(text=request.text, sentiment=request.sentiment)
    db.add(db_entry)
    db.commit()
    return db_entry


# Get the last text entry
@app.get("/texts/last", response_model=schemas.RetrieveTextEntry)  # Specifies response validation
def retrieve_last_text_entry(db: Session = Depends(get_db)):  # Specifies request validation
    db_entry = db.query(models.SentimentEntry).order_by(models.SentimentEntry.id.desc()).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="No entries found")
    return db_entry


# Get a text entry by ID
@app.get("/texts/{text_id}", response_model=schemas.RetrieveTextEntry)  # Specifies response validation
def retrieve_text_entry(text_id: int, db: Session = Depends(get_db)):  # Specifies request validation
    db_entry = db.query(models.SentimentEntry).filter(models.SentimentEntry.id == text_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")
    return db_entry


# Get all text entries
@app.get("/texts/", response_model=list[schemas.RetrieveTextEntry])  # Specifies response validation
def retrieve_all_text_entries(db: Session = Depends(get_db)):  # Specifies request validation
    return db.query(models.SentimentEntry).all()


@app.delete("/texts/", response_model=schemas.DeleteAllEntries)
def delete_all_text_entries(db: Session = Depends(get_db)):
    deleted_count = db.query(models.SentimentEntry).delete()  # Deletes all entries
    db.commit()
    return {"message": "All entries have been deleted.", "deleted_count": deleted_count}
