from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean, CheckConstraint
from datetime import datetime
from app.database import Base


class SentimentEntry(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)  # Ensure 'text' is defined
    sentiment = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Ensure database-level validation
    __table_args__ = (
        CheckConstraint('sentiment >= -1 AND sentiment <= 1', name='check_sentiment_range'),
        CheckConstraint('LENGTH(text) <= 500', name='check_text_length'))
