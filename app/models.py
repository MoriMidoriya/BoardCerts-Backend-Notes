from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(NoteBase):
    id: str
    created_at: datetime
    is_deleted: bool = False

    class Config:
        # Allows Pydantic to read data even if it's not a dict
        from_attributes = True