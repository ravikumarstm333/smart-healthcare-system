import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://ravikumarstm333_db_user:YVUI3c13RfAOdNXZ@cluster0.8tnbfur.mongodb.net/?appName=Cluster0")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smart_healthcare")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "f83a7c1d92b4e5f6a8c9d1e2f3a4b5c6")
SMS_API_KEY = os.getenv("SMS_API_KEY", "")
ALGORITHM = "HS256"
