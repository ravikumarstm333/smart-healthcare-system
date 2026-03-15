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

    prediction = model.predict(df)

    return int(prediction[0])