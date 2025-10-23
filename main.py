# main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from routers.zone import router as zones_router
from routers.vehicle import router as vehicles_router
from routers.user import router as users_router
from routers.parkingsession import router as parking_sessions_router
from models import Zone

app = FastAPI(title="API con Docker + Postgres + FastAPI")

def seed_zones():
    zones_data = [
        {"name": "Zona A", "rate_per_minute": 2, "max_minutes": 180},
        {"name": "Zona B", "rate_per_minute": 1, "max_minutes": 240},
        {"name": "Zona C", "rate_per_minute": 3, "max_minutes": 120},
    ]

    #Se abre una session, de que type: session
    with SessionLocal() as db:  
        existentes = {z.name for z in db.query(Zone).all()} #Evitamos duplicados :)
        nuevas = [Zone(**z) for z in zones_data if z["name"] not in existentes]

        if not nuevas:
            print("Zonas ya estaban sembradas.")
            return

        db.add_all(nuevas)
        db.commit()
        print("Zonas creadas.")

# Agregamos la funcion aqui para que se creen al arrancar la app
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_zones()

# Routers
app.include_router(zones_router)
app.include_router(vehicles_router)
app.include_router(users_router)
app.include_router(parking_sessions_router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hola Naomi :)"}
