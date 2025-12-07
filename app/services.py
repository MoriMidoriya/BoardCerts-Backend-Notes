from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from .models import NoteCreate, NoteUpdate

# Helper to format MongoDB document to Pydantic-friendly dict
def fix_id(doc):
    if doc:
        doc["id"] = str(doc["_id"])
        return doc
    return None

async def log_activity(db, note_id: str, action: str):
    """Simple Audit Log Implementation [cite: 26]"""
    await db.audit_logs.insert_one({
        "note_id": note_id,
        "action": action,
        "timestamp": datetime.utcnow()
    })

async def create_note(db, note: NoteCreate):
    note_data = note.dict()
    note_data.update({
        "created_at": datetime.utcnow(),
        "is_deleted": False  # Default for soft delete [cite: 25]
    })
    result = await db.notes.insert_one(note_data)
    
    # Audit Log
    await log_activity(db, str(result.inserted_id), "CREATE")
    
    return fix_id(await db.notes.find_one({"_id": result.inserted_id}))

async def get_note(db, note_id: str):
    try:
        oid = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Filter out soft-deleted notes [cite: 23]
    note = await db.notes.find_one({"_id": oid, "is_deleted": False})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return fix_id(note)

async def list_notes(db):
    cursor = db.notes.find({})
    notes = await cursor.to_list(length=100)
    return [fix_id(note) for note in notes]

async def update_note(db, note_id: str, update_data: NoteUpdate):
    try:
        oid = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    # Only update provided fields
    fields = {k: v for k, v in update_data.dict().items() if v is not None}
    
    if fields:
        result = await db.notes.update_one(
            {"_id": oid, "is_deleted": False}, 
            {"$set": fields}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Note not found or deleted")
        
        await log_activity(db, note_id, "UPDATE")

    return await get_note(db, note_id)

async def soft_delete_note(db, note_id: str):
    """Soft Delete Implementation [cite: 25]"""
    try:
        oid = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    # Do not remove from DB, just set flag to True
    result = await db.notes.update_one(
        {"_id": oid}, 
        {"$set": {"is_deleted": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    await log_activity(db, note_id, "SOFT_DELETE")
    return {"message": "Note soft deleted successfully"}