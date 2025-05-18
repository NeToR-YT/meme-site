from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Category(BaseModel):
    id: Optional[int] = None
    name: str

class Meme(BaseModel):
    id: Optional[int] = None
    title: str
    image_url: str
    category_id: int
    created_at: Optional[datetime] = None