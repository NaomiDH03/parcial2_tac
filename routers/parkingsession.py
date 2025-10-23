from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import ParkingSession
from schemas import ParkingSessionCreate, ParkingSessionOut

router = APIRouter(prefix="/parkingsessions", tags=["parkingsessions"])

@router.get("/", response_model=list[ParkingSessionOut])
def list_parking_sessions(db: Session = Depends(get_db)):
    return db.query(ParkingSession).all()

#Este es el start parking session
@router.post("/start", response_model=ParkingSessionOut, status_code=201)
def start_parking_session(session: ParkingSessionCreate, db: Session = Depends(get_db)):
    # Con estas líneas se verifica que que no haya una sesión activa con ste vehiculo
    active_session = db.query(ParkingSession).filter(
        ParkingSession.vehicle_id == session.vehicle_id,
        ParkingSession.status == 'active'
    ).first()
    if active_session:
        raise HTTPException(status_code=400, detail="Ya hay una sesión activa con este vehículo")
    
    new_session = ParkingSession(
        user_id=session.user_id,
        vehicle_id=session.vehicle_id,
        zone_id=session.zone_id,
        started_at=session.started_at,
        status='active'
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


#Ahora el stop de session con el id
@router.post("/stop/{session_id}", response_model=ParkingSessionOut)
def stop_parking_session(session_id: int, endes_at: str, db: Session = Depends(get_db)):
    session = db.query(ParkingSession).filter(ParkingSession.id == session_id).first()
    
    #Aqui van las reglas