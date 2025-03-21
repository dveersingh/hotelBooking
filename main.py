from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, engine, SessionLocal, UserModel, HotelRoom, BookingRecord
from utils import hash_password, check_password, generate_jwt, SegmentTree
from pydantic import BaseModel
from datetime import timedelta

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class RegisterUser(BaseModel):
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

class RoomDetails(BaseModel):
    room_number: str
    rate: float

class NewBooking(BaseModel):
    room_ref: int
    check_in_date: str
    check_out_date: str

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Registration
@app.post("/user/register")
def register_user(new_user: RegisterUser, db: Session = Depends(get_database)):
    encrypted_pw = hash_password(new_user.password)
    user_entry = UserModel(username=new_user.username, hashed_pw=encrypted_pw)
    db.add(user_entry)
    db.commit()
    return {"message": "User registered successfully."}

# User Login
@app.post("/user/login")
def authenticate_user(credentials: LoginUser, db: Session = Depends(get_database)):
    user = db.query(UserModel).filter(UserModel.username == credentials.username).first()
    if not user or not check_password(credentials.password, user.hashed_pw):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    token = generate_jwt({"sub": user.username}, timedelta(minutes=45))
    return {"access_token": token, "token_type": "bearer"}

# Add a new hotel room (Admin Only)
@app.post("/admin/rooms")
def add_room(room: RoomDetails, db: Session = Depends(get_database)):
    new_room = HotelRoom(room_number=room.room_number, rate=room.rate, occupied=False)
    db.add(new_room)
    db.commit()
    return {"message": "Room added successfully."}

# Get all rooms
@app.get("/rooms")
def get_rooms(db: Session = Depends(get_database)):
    return db.query(HotelRoom).all()

# Book a room
@app.post("/reservation")
def reserve_room(booking: NewBooking, db: Session = Depends(get_database)):
    selected_room = db.query(HotelRoom).filter(HotelRoom.id == booking.room_ref).first()
    if not selected_room or selected_room.occupied:
        raise HTTPException(status_code=400, detail="Room not available")
    selected_room.occupied = True
    new_booking = BookingRecord(client_id=1, room_ref=booking.room_ref, check_in_date=booking.check_in_date, check_out_date=booking.check_out_date)
    db.add(new_booking)
    db.commit()
    return {"message": "Room successfully booked."}

# View all bookings (Admin Only)
@app.get("/admin/reservations")
def view_reservations(db: Session = Depends(get_database)):
    return db.query(BookingRecord).all()

# Cancel a booking
@app.delete("/reservation/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_database)):
    booking = db.query(BookingRecord).filter(BookingRecord.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    room = db.query(HotelRoom).filter(HotelRoom.id == booking.room_ref).first()
    if room:
        room.occupied = False  # Mark room as available again

    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled successfully."}

# Dynamic Pricing API
@app.get("/dynamic-pricing")
def get_dynamic_rate(left: int, right: int, db: Session = Depends(get_database)):
    rates = [room.rate for room in db.query(HotelRoom).all()]
    seg_tree = SegmentTree(rates)
    return {"min_rate_in_range": seg_tree.query(0, 0, len(rates) - 1, left, right)}
