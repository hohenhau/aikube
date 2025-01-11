from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Base schema for a piece of text
# (Defines common fields for the text)
class TextBase(BaseModel):
    text: str


# Schema for creating a text entry
# (Used for request validation when creating an entry)
class TextCreate(TextBase):
    pass


# Schema for responding with an item
# (Adds the id field for responses)
class TextAnalysis(TextBase):
    id: int
    sentiment: Optional[float] = Field(None, ge=-1.0, le=1.0)  # validates between -1 and 1
    processed: bool
    timestamp: datetime

    class Config:
        from_attributes = True