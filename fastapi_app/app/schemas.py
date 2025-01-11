from pydantic import BaseModel


# Schema for analysing text (ML model response)
class AnalyseText(BaseModel):
    text: str
    sentiment: float

    class Config:
        schema_extra = {
            "example": {
                "text": "Example Text",
                "sentiment": 0.0}}


# Schema for analysing and adding text (combined functionality)
class AnalyseAndAddText(BaseModel):
    text: str
    sentiment: float

    class Config:
        schema_extra = {
            "example": {
                "text": "Example Text",
                "sentiment": 0.0}}


# Schema for adding text and sentiment (manual entry)
class AddText(BaseModel):
    text: str
    sentiment: float

    class Config:
        schema_extra = {
            "example": {
                "text": "Example Text",
                "sentiment": 0.0}}


# Schema for reading text entries from the database
class RetrieveTextEntry(BaseModel):
    id: int
    text: str
    sentiment: float

    class Config:
        from_attributes = True

