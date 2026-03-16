from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.health_routes import router as health_router
from routes.appointment_routes import router as appointment_router

app = FastAPI(
    title="Smart Healthcare Monitoring API",
    description="API for user authentication, health prediction, and doctor appointments.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(health_router, tags=["Health Prediction"])
app.include_router(appointment_router, tags=["Appointments"])

@app.get("/", tags=["Health Check"])
def home():
    return {"message": "Smart Healthcare API is running smoothly."}