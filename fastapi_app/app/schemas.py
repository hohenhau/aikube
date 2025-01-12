from pydantic import BaseModel


class AnalyseAndOrAddText(BaseModel):
    text: str
    sentiment: float | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
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


# Schema for deleting all entries from the database
class DeleteAllEntries(BaseModel):
    message: str
    deleted_count: int
