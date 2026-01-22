from fastapi import APIRouter, Depends, HTTPException, Body, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models.user import User
from app.models.log import Log, LogAnalysis
from app.schemas.log import LogOut, LogCreate, LogAnalysisOut
from app.core.log_analyzer import LogAnalyzer
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
)

@router.post("/raw", response_model=LogOut)
def create_log_raw(
    content: str = Body(..., media_type="text/plain"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = Log(
        owner_id=current_user.id,
        content=content,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.post("/raw/analyze", response_model=LogAnalysisOut)
def create_and_analyze_log_raw(
    content: str = Body(..., media_type="text/plain"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        log = Log(owner_id=current_user.id, content=content)
        db.add(log)
        db.flush()

        analysis = LogAnalyzer.analyze_log(db=db, log_id=log.id, log_text=log.content)

        db.commit()
        db.refresh(analysis)
        return analysis

    except Exception:
        db.rollback()
        raise


@router.post("/", response_model=LogOut)
def create_log(
    payload: LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = Log(
        owner_id=current_user.id,
        content=payload.content,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.post("/{log_id:int}/analyze", response_model=LogAnalysisOut)
def analyze_existing_log(
        log_id: int,
        db: Session =  Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    log = db.query(Log).filter(
        Log.id == log_id,
        Log.owner_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    analysis = LogAnalyzer.analyze_log(
        db=db,
        log_id=log.id,
        log_text=log.content
    )
    db.commit()
    db.refresh(analysis)
    return analysis


@router.post("/analyze", response_model=LogAnalysisOut)
def create_and_analyze_log(
    payload: LogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        log = Log(owner_id=current_user.id, content=payload.content)
        db.add(log)
        db.flush()

        analysis = LogAnalyzer.analyze_log(db=db, log_id=log.id, log_text=log.content)

        db.commit()
        db.refresh(analysis)
        return analysis

    except Exception:
        db.rollback()
        raise


@router.get("/{log_id:int}/analysis", response_model=LogAnalysisOut)
def get_log_analysis(
        log_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    log = db.query(Log).filter(
        Log.id == log_id,
        Log.owner_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    analysis = db.query(LogAnalysis).filter(LogAnalysis.log_id == log.id).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis for this log yet")

    return analysis


@router.get("/", response_model=List[LogOut])
def list_user_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Log)
        .filter(Log.owner_id == current_user.id)
        .order_by(Log.created_at.desc())
        .all()
    )

@router.delete("/{log_id:int}/", status_code=status.HTTP_200_OK)
def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = db.query(Log).filter(
        Log.id == log_id,
        Log.owner_id == current_user.id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return {"deleted": True, "log_id": log_id}