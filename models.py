from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

DB_URL = "sqlite:///./hotel_management.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_pw = Column(String)

class HotelRoom(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True)
    rate = Column(Float)
    occupied = Column(Boolean, default=False)

class BookingRecord(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    room_ref = Column(Integer, ForeignKey("rooms.id"))
    check_in_date = Column(String)
    check_out_date = Column(String)
    customer = relationship("UserModel")
    room = relationship("HotelRoom")
