from fastapi import APIRouter, Depends
from typing import List
from .database import get_database
from .models import NoteCreate, NoteResponse, NoteUpdate
from . import services

router = APIRouter()

@router.post("/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate, db = Depends(get_database)):
    return await services.create_note(db, note)

@router.get("/notes", response_model=List[NoteResponse])
async def read_notes(db = Depends(get_database)):
    return await services.list_notes(db)

@router.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note(note_id: str, db = Depends(get_database)):
    return await services.get_note(db, note_id)

@router.patch("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note: NoteUpdate, db = Depends(get_database)):
    return await services.update_note(db, note_id, note)

@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, db = Depends(get_database)):
    return await services.soft_delete_note(db, note_id)