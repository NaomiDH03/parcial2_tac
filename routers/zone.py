from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Zone
from schemas import ZoneParking

router = APIRouter(prefix="/zones", tags=["zones"])

@router.get("/", response_model=list[ZoneParking])
def list_zones(db: Session = Depends(get_db)):
    return db.query(Zone).all()