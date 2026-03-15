from fastapi import APIRouter
from schemas.models import HealthInput
from services.prediction_service import predict_disease
from services.sms_service import send_high_risk_alert
from database import prediction_collection

router = APIRouter()

@router.post("/predict")
def predict(data: HealthInput):
    input_data = data.dict()
    result = predict_disease(input_data)
    
    risk = "Low Risk"
    if result == 1:
        risk = "High Risk"
        # Trigger SMS alert for high risk predictions
        send_high_risk_alert(
            phone_number="[USER_PHONE]",
            message="Your recent health prediction indicates a High Risk. Please book an appointment with a doctor via your SmartHealth dashboard immediately."
        )

    prediction_collection.insert_one({
        "input": input_data,
        "risk": risk
    })

    return {
        "prediction": result,
        "risk": risk
    }
