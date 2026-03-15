import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smart_healthcare")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_healthcare_key")
SMS_API_KEY = os.getenv("SMS_API_KEY", "")
ALGORITHM = "HS256"
