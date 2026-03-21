from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path

from app.models.user import User
from app.api.dependencies.auth import get_current_user

import shutil
import uuid



#Main route
router = APIRouter(prefix="/datasets", tags=["datasets"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

#File upload endpoints

#Generic File upload endpoint
@router.post("upload")
async def uploadfile(current_user: User = Depends(get_current_user), file: UploadFile = File(...)):
    
    #Basic validation of a filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename was provided.")
    
    #Adds an unique filename to store it and prevent overwriting
    extension = Path(file.filename).suffix
    storage_filename = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / storage_filename
    
    #Saves the file in directory
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    return{
        "original_filename": file.filename,
        "storage_filename": storage_filename,
        "content_type": file.content_type
    }

#Fil