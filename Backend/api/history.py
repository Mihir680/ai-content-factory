from fastapi import APIRouter
from sqlalchemy.orm import Session

from Backend.database.database import SessionLocal
from Backend.database.models import Content

router = APIRouter()


@router.get("/history")
def get_history():
    db: Session = SessionLocal()

    try:
        history = db.query(Content).order_by(Content.id.desc()).limit(5).all()
        return history


    finally:
        db.close()