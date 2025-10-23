from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Vehicle
from schemas import VehicleCreate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/", response_model=list[VehicleCreate])
def list_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()
 
#El post jala cuando un user con el id ya existe
@router.post("/", response_model=VehicleCreate)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.plate == vehicle.plate).first()
    if db_vehicle:
        raise HTTPException(status_code=400, detail="El vehículo ya existe.")
    
    new_vehicle = Vehicle(user_id=vehicle.user_id, plate=vehicle.plate)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle