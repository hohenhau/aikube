import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Initialise the FastAPI app
app = FastAPI()


# Analyse a piece of text
@app.post("/analyse_text")
async def analyse_text(text: str, db: Session = Depends(get_db)):
    sentiment = await analyse_sentiment(text)  # Call ML model to get sentiment
    return {"text": text, "sentiment": sentiment['sentiment'], "label": sentiment['label']}


# Analyse and add a piece of text to the database
@app.post("/analyse_and_add_text")
async def analyse_and_add_text(text: str, db: Session = Depends(get_db)):
    sentiment = await analyse_sentiment(text)  # Call ML model to get sentiment
    # Create new entry with text and sentiment
    new_entry = models.YourModel(text=text, sentiment=sentiment['sentiment'])
    db.add(new_entry)
    db.commit()
    return {"message": "Entry added", "text": text, "sentiment": sentiment['sentiment'], "label": sentiment['label']}


# Add a piece of text and its sentiment value (between 0 and 1) to the database
@app.post("/add_text")
async def add_text(text: str, sentiment: float, db: Session = Depends(get_db)):
    if not (-1 <= sentiment <= 1):
        raise HTTPException(status_code=400, detail="Sentiment value must be between -1 and 1")
    new_entry = models.YourModel(text=text, sentiment=sentiment)
    db.add(new_entry)
    db.commit()
    return {"message": "Entry added", "text": text, "sentiment": sentiment}


# Get a text entry by ID
@app.get("/texts/{text_id}", response_model=schemas.TextAnalysis)
def read_text_entry(text_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(models.Item).filter(models.Item.id == text_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")
    return db_entry


# Get all text entries
@app.get("/texts/", response_model=list[schemas.TextAnalysis])
def read_all_text_entries(db: Session = Depends(get_db)):
    return db.query(models.Item).all()
