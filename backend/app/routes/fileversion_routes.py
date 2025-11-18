from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from zipfile import ZipFile
from io import BytesIO
from ..db import get_session, _import_models
from ..models import file_version, file
from ..utils.logger import log_action

router = APIRouter(prefix="/api/files", tags = ["Files"])

@router.get("/{file_id}/versions")
def list_file_versions(file_id: int, db: Session = Depends(get_session)):
    versions = db.query(file_version.FileVersion).filter(file_version.FileVersion.file_id == file_id).all()
    
    if not versions:
        raise HTTPException(status_code=404, detail="File or versions not found")

    return [
        {
            "version": v.version_number, 
            "size": v.size, 
            "uploaded_at": v.uploaded_at.isoformat() if v.uploaded_at else None,
            "filepath": v.filepath,
            "notes": v.notes
        } 
        for v in versions
    ]

@router.post("/download-zip")
def download_zip(file_id: List[int], db: Session = Depends(get_session)):

    files = db.query(file.File).filter(file.File.id.in_(file.file_ids)).all()

    if not files:
        raise HTTPException(status_code=404, detail="No files found for the given ID")
    
    zbuffer = BytesIO
    with ZipFile(zbuffer, 'w') as zip_file:
        for file in files:
            try:
                mock = f"Content of file {file.filename} with version: {file.current_version})"
                zip_file.writestr(file.filename, mock)
                log_action(user_id=1, action='download', file_id=file.id, details={"zip_part": True})
            except Exception as e:
                print(f"Error during archiving file {file.filename}: {e}")
    zbuffer.seek(0)

    return Response(
        content=zbuffer.read(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=files_download.zip"}
    )
    

@router.post("/{file_id}/rollback/{version_number}")
def rollback_file_version(file_id: int, version_number: int, db: Session = Depends(get_session)):
    target_ver = db.query(file_version.FileVersion).filter(file_version.FileVersion.file_id == file_id, file_version.FileVersion.version_number == version_number).first()

    if not target_ver:
        raise HTTPException(status_code=404, detail="Version not found")
    
    cur_file =  db.query(file.File).filter(file.File.file_id == file_id).first()

    if not cur_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    cur_file.filepath = target_ver.filepath
    cur_file.size = target_ver.size
    cur_file.current_version = target_ver.version_number
    
    db.commit()
    log_action(user_id=1, action="rollback", file_id=file_id, details={"rolled_back_to": version_number}) #Mock rollback

    return {"message": f"File {file_id} rolled back to version {version_number}"}