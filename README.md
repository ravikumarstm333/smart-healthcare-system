# Smart Healthcare System

A full-stack healthcare application featuring a React frontend and a FastAPI Python backend.

## Project Structure

- `frontend/`: React application providing the user interface (Dashboards, Booking forms, Auth, etc.).
- `backend/`: FastAPI application handling API requests, database interactions, and machine learning models.

## Prerequisites

To run this project, you will need:
- **Node.js** (v14 or higher recommended) for the React frontend
- **Python** (v3.8 or higher) for the FastAPI backend

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd smart-healthcare-system
```

### 2. Backend Setup
Open a terminal and navigate to the backend directory.

```bash
cd backend

# Create a virtual environment (optional but recommended)
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Set up your environment variables
# Copy the example environment file and update your variables (e.g., database URLs, secrets)
cp exaple.envfile .env
# Note: On Windows Command Prompt, use: copy exaple.envfile .env

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*The API will be available at `http://localhost:8000`. You can view the interactive API documentation at `http://localhost:8000/docs`.*

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory.

```bash
cd frontend

# Install the Node.js dependencies
npm install

# Start the React development server
npm start
```
*The application UI will be available at `http://localhost:3000`.*

## Features
- **User Authentication**: Secure login and registration.
- **Doctor Booking**: Interactive booking interface for scheduling appointments.
- **Health Form**: Easy submission of health-related information.
- **Dashboard**: Overview and management of user and health data.

## Note
Files like `node_modules/`, `.venv/`, and `.env` are deliberately excluded from this repository (via `.gitignore`) to keep the repository clean and secure. Be sure to run through the full setup locally to generate these missing dependencies and environment files.
