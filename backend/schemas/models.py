from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Appointment(BaseModel):
    username: str
    doctor_name: str
    specialization: str
    date: str
    time: str

class HealthInput(BaseModel):
    age: int
    gender: int
    bmi: float
    daily_steps: int
    sleep_hours: float
    water_intake_l: float
    calories_consumed: int
    smoker: int
    alcohol: int
    resting_hr: int
    systolic_bp: int
    diastolic_bp: int
    cholesterol: int
    family_history: int
