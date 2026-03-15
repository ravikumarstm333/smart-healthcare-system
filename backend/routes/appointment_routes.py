from fastapi import APIRouter
from schemas.models import Appointment
from database import appointments_collection

router = APIRouter()

@router.get("/doctors")
def get_doctors():
    # Mock list of doctors
    return [
        {"id": 1, "name": "Dr. Sarah Jenkins", "specialization": "Cardiologist", "hospital": "City Heart Center", "available_times": ["09:00 AM", "11:00 AM", "02:00 PM"]},
        {"id": 2, "name": "Dr. Rajesh Kumar", "specialization": "General Physician", "hospital": "Apollo Clinic", "available_times": ["10:00 AM", "01:00 PM", "04:00 PM"]},
        {"id": 3, "name": "Dr. Emily Chen", "specialization": "Endocrinologist", "hospital": "Metro Healthcare", "available_times": ["09:30 AM", "03:00 PM", "05:00 PM"]},
        {"id": 4, "name": "Dr. Michael Brown", "specialization": "Neurologist", "hospital": "Brain & Spine Institute", "available_times": ["11:30 AM", "02:30 PM", "04:30 PM"]}
    ]

@router.post("/book_appointment")
def book_appointment(appt: Appointment):
    appointment_data = appt.dict()
    appointments_collection.insert_one(appointment_data)
    return {"message": "Appointment booked successfully"}
