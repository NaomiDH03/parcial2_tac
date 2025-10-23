from pydantic import BaseModel, EmailStr

#Esquema de mi tabla zone
class ZoneParking(BaseModel):
    name: str
    rate_per_minute: int
    max_minutes: int


#Esquema de mi tabla vehicle
class VehicleCreate(BaseModel):
    user_id: int
    plate: str

    class Config:
        orm_mode = True #Lo pongo porque esta va a ser un post

#Esquema de los usuarios
class UserIn(BaseModel):
    name: str
    email: EmailStr
    api_key: str
    balance: int = 300

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

#Esquema de Parking session

class ParkingSessionCreate(BaseModel):
    user_id: int
    vehicle_id: int
    zone_id: int
    started_at: str

class ParkingSessionOut(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    zone_id: int
    started_at: str
    endes_at: str | None = None
    minutes: int | None = None
    cost: int | None = None
    status: str

    class Config:
        orm_mode = True


