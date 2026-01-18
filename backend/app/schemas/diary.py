from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# --- Client Schemas ---
class ClientBase(BaseModel):
    full_name: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Case Schemas ---
class CaseBase(BaseModel):
    case_number: str
    court: str
    case_type: str
    stage: Optional[str] = None
    filing_date: Optional[date] = None
    status: Optional[str] = "Active"

class CaseCreate(CaseBase):
    client_id: int

class Case(CaseBase):
    id: int
    client_id: int
    next_hearing: Optional[date] = None
    created_at: datetime
    
    # We can include client details optionally
    client: Optional[Client] = None

    class Config:
        from_attributes = True


# --- Hearing Schemas ---
class HearingBase(BaseModel):
    hearing_date: date
    purpose: Optional[str] = None
    order_passed: Optional[str] = None
    next_date: Optional[date] = None
    remarks: Optional[str] = None

class HearingCreate(HearingBase):
    case_id: int

class Hearing(HearingBase):
    id: int
    case_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    due_date: Optional[date] = None
    status: Optional[str] = "Pending"
    priority: Optional[str] = "Medium"

class TaskCreate(TaskBase):
    case_id: Optional[int] = None

class Task(TaskBase):
    id: int
    case_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# --- Fee Schemas ---
class FeeBase(BaseModel):
    amount_billed: float = 0.0
    amount_received: float = 0.0
    date: date
    description: Optional[str] = None

class FeeCreate(FeeBase):
    case_id: int

class Fee(FeeBase):
    id: int
    case_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# --- Dashboard / Report Schemas ---
class DashboardStats(BaseModel):
    hearings_today: int
    cases_pending: int
    tasks_due_today: int
    fees_outstanding: float
    upcoming_hearings: List[Hearing]
