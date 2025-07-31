from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.table import Table, TableStatus
from app.models.table_session import TableSession
from app.models.user import User
from app.schemas.table import TableResponse, TableSessionCreate, TableSessionResponse, TableWithSession
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=List[TableResponse])
def get_all_tables(db: Session = Depends(get_db)):
    """Get all tables"""
    tables = db.query(Table).filter(Table.is_active == True).all()
    return tables


@router.get("/available", response_model=List[TableResponse])
def get_available_tables(db: Session = Depends(get_db)):
    """Get all available tables"""
    tables = db.query(Table).filter(
        Table.is_active == True,
        Table.status == TableStatus.AVAILABLE
    ).all()
    return tables


@router.get("/{table_number}", response_model=TableWithSession)
def get_table_by_number(table_number: str, db: Session = Depends(get_db)):
    """Get table by table number"""
    table = db.query(Table).filter(
        Table.table_number == table_number,
        Table.is_active == True
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    return table


@router.post("/{table_number}/start-session", response_model=TableSessionResponse)
def start_table_session(
    table_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new table session"""
    # Check if table exists and is available
    table = db.query(Table).filter(
        Table.table_number == table_number,
        Table.is_active == True
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    if table.status != TableStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Table is not available"
        )
    
    # Check if user already has an active session
    existing_session = db.query(TableSession).filter(
        TableSession.user_id == current_user.id,
        TableSession.is_active == True
    ).first()
    
    if existing_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active session at another table"
        )
    
    # Create new session
    session = TableSession(
        table_id=table.id,
        user_id=current_user.id
    )
    db.add(session)
    
    # Update table status
    table.status = TableStatus.OCCUPIED
    
    db.commit()
    db.refresh(session)
    
    return session


@router.post("/{table_number}/end-session")
def end_table_session(
    table_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End the current table session"""
    # Find the table
    table = db.query(Table).filter(
        Table.table_number == table_number,
        Table.is_active == True
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    # Find active session for this user at this table
    session = db.query(TableSession).filter(
        TableSession.table_id == table.id,
        TableSession.user_id == current_user.id,
        TableSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active session found for this table"
        )
    
    # End the session
    session.is_active = False
    session.session_end = datetime.utcnow()
    
    # Update table status
    table.status = TableStatus.AVAILABLE
    
    db.commit()
    
    return {"message": "Session ended successfully"}


@router.get("/session/current", response_model=TableSessionResponse)
def get_current_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current active session for the user"""
    session = db.query(TableSession).filter(
        TableSession.user_id == current_user.id,
        TableSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active session found"
        )
    
    return session


@router.post("/qr/{table_number}/scan")
def scan_table_qr(
    table_number: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Scan QR code for table (same as start session)"""
    return start_table_session(table_number, current_user, db) 