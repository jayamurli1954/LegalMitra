from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    mobile = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cases = relationship("Case", back_populates="client")


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String, index=True)
    court = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))
    case_type = Column(String)  # Civil, Criminal, etc.
    stage = Column(String, nullable=True) # Trial, Evidence, etc.
    filing_date = Column(Date, nullable=True)
    next_hearing = Column(Date, nullable=True)
    status = Column(String, default="Active") # Active, Disposed
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="cases")
    hearings = relationship("Hearing", back_populates="case")
    tasks = relationship("Task", back_populates="case")
    fees = relationship("Fee", back_populates="case")


class Hearing(Base):
    __tablename__ = "hearings"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    hearing_date = Column(Date, index=True)
    purpose = Column(String, nullable=True) # Evidence, Arguments
    order_passed = Column(Text, nullable=True)
    next_date = Column(Date, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="hearings")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True) # Can be general task
    title = Column(String)
    due_date = Column(Date, nullable=True)
    status = Column(String, default="Pending") # Pending, Completed
    priority = Column(String, default="Medium") # High, Medium, Low
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="tasks")


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    amount_billed = Column(Float, default=0.0)
    amount_received = Column(Float, default=0.0)
    date = Column(Date, default=datetime.utcnow)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="fees")
