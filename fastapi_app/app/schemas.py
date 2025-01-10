from pydantic import BaseModel


# Base schema for an item
# (Defines common fields for the Item)
class ItemBase(BaseModel):
    name: str
    description: str
    price: float


# Schema for creating an item
# (Used for request validation when creating an item)
class ItemCreate(ItemBase):
    pass


# Schema for responding with an item
# (Adds the id field for responses)
class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True
