from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, health_routes, appointment_routes

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
app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(health_routes.router, tags=["Health Prediction"])
app.include_router(appointment_routes.router, tags=["Appointments"])

@app.get("/", tags=["Health Check"])
def home():
    return {"message": "Smart Healthcare API is running smoothly."}