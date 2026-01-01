from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime

from app.core.database import get_db
from app.models import diary as models
from app.schemas import diary as schemas

router = APIRouter()

# --- Dashboard ---
@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get statistics for the dashboard widget"""
    today = date.today()
    
    # Hearings today
    hearings_today_count = db.query(models.Hearing).filter(models.Hearing.hearing_date == today).count()
    
    # Active/Pending cases (Status != Disposed)
    cases_pending_count = db.query(models.Case).filter(models.Case.status != "Disposed").count()
    
    # Tasks due today or earlier (overdue) and not completed
    tasks_due_count = db.query(models.Task).filter(
        models.Task.due_date <= today,
        models.Task.status != "Completed"
    ).count()
    
    # Fees outstanding (Billed - Received) across all cases
    # SQL alchemy sum calculation or python logic
    all_fees = db.query(models.Fee).all()
    total_outstanding = sum([f.amount_billed - f.amount_received for f in all_fees])
    
    # Upcoming hearings for the next 7 days
    upcoming_hearings = db.query(models.Hearing).filter(
        models.Hearing.hearing_date >= today
    ).order_by(models.Hearing.hearing_date.asc()).limit(5).all()

    return schemas.DashboardStats(
        hearings_today=hearings_today_count,
        cases_pending=cases_pending_count,
        tasks_due_today=tasks_due_count,
        fees_outstanding=total_outstanding,
        upcoming_hearings=upcoming_hearings
    )

# --- Clients ---
@router.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/clients", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(models.Client).offset(skip).limit(limit).all()
    return clients

# --- Cases ---
@router.post("/cases", response_model=schemas.Case)
def create_case(case: schemas.CaseCreate, db: Session = Depends(get_db)):
    db_case = models.Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.get("/cases", response_model=List[schemas.Case])
def read_cases(skip: int = 0, limit: int = 100, status: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Case)
    if status:
        query = query.filter(models.Case.status == status)
    cases = query.order_by(models.Case.next_hearing.asc()).offset(skip).limit(limit).all()
    return cases

@router.get("/cases/{case_id}", response_model=schemas.Case)
def read_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

# --- Hearings (The Auto Diary) ---
@router.post("/hearings", response_model=schemas.Hearing)
def log_hearing(hearing: schemas.HearingCreate, db: Session = Depends(get_db)):
    # 1. Add hearing record
    db_hearing = models.Hearing(**hearing.dict())
    db.add(db_hearing)
    
    # 2. Auto-update Case's next_hearing date
    case = db.query(models.Case).filter(models.Case.id == hearing.case_id).first()
    if case and hearing.next_date:
        case.next_hearing = hearing.next_date
    
    db.commit()
    db.refresh(db_hearing)
    return db_hearing

@router.get("/hearings", response_model=List[schemas.Hearing])
def read_hearings_by_case(case_id: int, db: Session = Depends(get_db)):
    return db.query(models.Hearing).filter(models.Hearing.case_id == case_id).order_by(models.Hearing.hearing_date.desc()).all()

# --- Tasks ---
@router.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/{case_id}", response_model=List[schemas.Task])
def read_tasks_by_case(case_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.case_id == case_id).all()

# --- Fees ---
@router.post("/fees", response_model=schemas.Fee)
def log_fee(fee: schemas.FeeCreate, db: Session = Depends(get_db)):
    db_fee = models.Fee(**fee.dict())
    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return db_fee

@router.get("/fees/{case_id}", response_model=List[schemas.Fee])
def read_fees_by_case(case_id: int, db: Session = Depends(get_db)):
    return db.query(models.Fee).filter(models.Fee.case_id == case_id).all()
