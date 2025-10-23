from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    balance = Column(Integer, default=300)
    
    # Relaciones que el user tiene
    #Parametros relationship ("nombre de la clase", back_populates="es el atributo con el que se relaciona")
    vehicles = relationship("Vehicle", back_populates="user")
    parking_sessions = relationship("ParkingSession", back_populates="user")

class Zone(Base):
    __tablename__ = 'zones'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rate_per_minute = Column(Integer)
    max_minutes = Column(Integer)

    # Obvio esta tiene relacion con parking sessions
    parking_sessions = relationship("ParkingSession", back_populates="zone")

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    plate = Column(String, unique=True, index=True)

    # Claramente el vechículo tiene relacion con el usuario y donde parkeo
    user = relationship("User", back_populates="vehicles")
    parking_sessions = relationship("ParkingSession", back_populates="vehicle")

class ParkingSession(Base):
    __tablename__ = 'parking_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), index=True)
    started_at = Column(String)
    endes_at = Column(String, nullable=True)
    minutes = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
    status = Column(String, default='active')  #Ponemos en default que esta activo (chance y esto lo cambie)

    # Relaciones igual que en las demás
    user = relationship("User", back_populates="parking_sessions")
    vehicle = relationship("Vehicle", back_populates="parking_sessions")
    zone = relationship("Zone", back_populates="parking_sessions")
