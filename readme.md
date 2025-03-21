# Hotel Booking Backend

## Overview
This is a **FastAPI**-based backend system for a hotel booking application. It allows users to **register, login, book rooms, cancel bookings**, and provides **dynamic pricing** for hotel rooms using a **Segment Tree**. The system uses **SQLite** as the database and features authentication via **JWT tokens**.

## Features
- **User Management:** Register and login with hashed passwords.
- **Room Management:** Add, view, and manage hotel rooms.
- **Booking System:** Book and cancel hotel room reservations.
- **Authentication:** Secure JWT-based user authentication.
- **Admin Functions:** View all reservations, add rooms.
- **Dynamic Pricing:** Get the minimum room rate in a specified range using Segment Tree.

---

## Project Structure
```
.
├── main.py        # FastAPI app with endpoints
├── models.py      # Database models using SQLAlchemy
├── utils.py       # Helper functions (JWT, password hashing, Segment Tree)
├── requirements.txt # Required dependencies
└── README.md      # Project documentation
```

---

## Installation & Setup
### **1. Clone the Repository**
```sh
git clone https://github.com/dveersingh/hotelBooking.git
cd hotelBooking
```
### **2. Create a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```
### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```
### **4. Run the FastAPI Server**
```sh
uvicorn main:app --reload
```

---

## API Endpoints
### **User Management**
| Method | Endpoint | Description |
|--------|------------|-------------|
| `POST` | `/user/register` | Register a new user |
| `POST` | `/user/login` | Login and get JWT token |

### **Room Management**
| Method | Endpoint | Description |
|--------|------------|-------------|
| `POST` | `/admin/rooms` | Add a new hotel room (Admin Only) |
| `GET` | `/rooms` | View all hotel rooms |

### **Booking System**
| Method | Endpoint | Description |
|--------|------------|-------------|
| `POST` | `/reservation` | Book a hotel room |
| `DELETE` | `/reservation/{booking_id}` | Cancel a booking |
| `GET` | `/admin/reservations` | View all bookings (Admin Only) |

### **Dynamic Pricing**
| Method | Endpoint | Description |
|--------|------------|-------------|
| `GET` | `/dynamic-pricing?left=0&right=2` | Get minimum room rate in range |

---

## Database Models
- **UserModel**: Stores user credentials.
- **HotelRoom**: Represents available hotel rooms.
- **BookingRecord**: Tracks room reservations.

---

## Authentication
- Users must **login** to receive a **JWT token**.
- The token must be included in API requests for authentication.

Example token response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
}
```

---

## Dependencies
- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for running FastAPI.
- **SQLAlchemy**: ORM for database interactions.
- **Passlib & Bcrypt**: Secure password hashing.
- **Python-JOSE**: JWT authentication handling.

To install all dependencies:
```sh
pip install -r requirements.txt
```

---

## Running with Docker (Optional)
1. **Build the Docker Image**
```sh
docker build -t hotel-booking-backend .
```
2. **Run the Container**
```sh
docker run -p 8000:8000 hotel-booking-backend
```

---

## Future Improvements
- Implement **role-based access control (RBAC)**.
- Add **Stripe payment integration**.
- Enhance **room availability logic**.

---

## GitHub Repository
[Hotel Booking Backend](https://github.com/dveersingh/hotelBooking)

---

## License
This project is open-source and free to use.

---

## Contact
For any queries, reach out to **[Dharmveer Singh]** at **veersinghmau@gmail.com**.

