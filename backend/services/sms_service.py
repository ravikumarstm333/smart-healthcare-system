import time

def send_high_risk_alert(phone_number: str, message: str):
    """
    Mock SMS Service. In production, this would use Twilio or a similar API.
    """
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔥 URGENT ALERT TRIGGERED 🔥")
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print("------------------------------------------------------------------\n")
    return True
