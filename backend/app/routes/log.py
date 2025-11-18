from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional, List
import csv
from io import StringIO
from datetime import datetime, date
from ..db import get_session
from ..models.log_book import LogBook

router = APIRouter(prefix="/api/logbook", tags = ["LogBook"])

def get_current_admin_user():

    is_admin = True

    if not is_admin:
        raise HTTPException(status_code=403, detail="Restricted admin page")
    return {"user_id": 1, "role": "admin"} #Mock admin

@router.get("/")
def get_logbook_entries(user_id: Optional[int] = Query(None, description="Filter by user ID"),
                        action: Optional[str] = Query(None, description="Filter by action type"),
                        start_date: Optional[date] = Query(None, description="Filter by starting date"),
                        end_date: Optional[date] = Query(None, description="Filter by ending date"),
                        sort_by: str = Query("timestamp_desc", description="Sortt by timestamp"),
                        db: Session = Depends(get_session),
                        admin_user: dict = Depends(get_current_admin_user)):
    query = db.query(LogBook)

    if user_id is not None:
        query = query.filter(LogBook.user_id == user_id)
    if action:
        query = query.filter(LogBook.action == action)
    if start_date:
        query = query.filter(LogBook.timestamp >= start_date)
    if end_date:
        next_day = end_date + datetime.timedelta(days=1)
        query = query.filter(LogBook.timestamp < next_day)

    if sort_by == "timestamp_asc":
        query = query.order_by(LogBook.timestamp.asc())
    else:
        query = query.order_by(LogBook.timestamp.desc())
    
    entries = query.all()

    return[

        {
            "id": entry.id,
            "user_id": entry.user_id,
            "action": entry.action,
            "timestamp": entry.timestamp.isoformat(),
            "file_id": entry.file_id,
            "details": entry.details
        }
        for entry in entries
    ]

@router.get("/stats")
def get_logbook_stats(db: Session = Depends(get_session)):
    action_counts = db.query(LogBook.action, func.count(LogBook.id)).group_by(LogBook.action).all()

    stats={f"total_{action}s": count for action, count in action_counts}

    unique_users = db.query(func.count(LogBook.user_id.distinct())).scalar() #Exemplary stat
    stats["total_unique_users"] = unique_users
    
    return stats

@router.get("/export", response_class=Response, name="export_logbook_to_csv")
def export_logbook_to_csv(db: Session = Depends(get_session)):
    entries = db.query(LogBook).order_by(LogBook.timestamp.desc()).all()

    if not entries:
        raise HTTPException(status_code=404, detail="No log entries")
    
    output=StringIO()
    fieldnames = ['id', 'user_id', 'action', 'timestamp', 'file_id', 'details']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for entry in entries:
        writer.writerow({
            'id': entry.id,
            'user_id': entry.user_id,
            'action': entry.action,
            'timestamp': entry.timestamp.isoformat() if entry.timestamp else '',
            'file_id': entry.file_id,
            'details': str(entry.details)
        })
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=logbook_export.csv"}
    )