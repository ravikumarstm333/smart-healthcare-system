import joblib
import pandas as pd

model = joblib.load("models/health_model.pkl")

feature_columns = [
    "age","gender","bmi","daily_steps","sleep_hours",
    "water_intake_l","calories_consumed","smoker",
    "alcohol","resting_hr","systolic_bp","diastolic_bp",
    "cholesterol","family_history"
]

def predict_disease(data):

    df = pd.DataFrame([data])
    df = df[feature_columns]

    # probability
    probabilities = model.predict_proba(df)[0]

    high_risk_percent = round(probabilities[1] * 100, 2)

    # decision rule
    if high_risk_percent <= 40:
        recommendation = "Home Care Advice"
    else:
        recommendation = "Doctor Appointment Required"

    return {
        "risk_percent": high_risk_percent,
        "recommendation": recommendation
    }