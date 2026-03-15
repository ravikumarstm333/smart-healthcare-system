import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Activity } from "lucide-react";
import Auth from "./Auth";
import Dashboard from "./Dashboard";
import HealthForm from "./HealthForm";
import DoctorBooking from "./DoctorBooking";
import "./App.css";

const ProtectedRoute = ({ isAuthenticated, children }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setIsAuthenticated(false);
  };

  if (loading) return null;

  return (
    <Router>
      <div className="app-container">
        <header className="header" style={{ marginBottom: "2rem" }}>
          <Activity size={48} className="header-icon" />
          <h1 className="title" style={{ fontSize: "2rem" }}>SmartHealth Predictor</h1>
          <p className="subtitle" style={{ fontSize: "1rem" }}>AI-Powered Lifestyle & Disease Risk Analysis</p>
        </header>

        <main style={{ width: "100%", display: "flex", justifyContent: "center" }}>
          <Routes>
            <Route 
              path="/login" 
              element={isAuthenticated ? <Navigate to="/dashboard" /> : <Auth onLogin={handleLogin} />} 
            />
            
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute isAuthenticated={isAuthenticated}>
                  <Dashboard onLogout={handleLogout} />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/predict" 
              element={
                <ProtectedRoute isAuthenticated={isAuthenticated}>
                  <div className="form-card">
                    <button 
                      onClick={() => window.location.href = "/dashboard"} 
                      style={{ background: "transparent", color: "var(--primary)", border: "none", cursor: "pointer", marginBottom: "1rem", fontWeight: "600" }}
                    >
                      ← Back to Dashboard
                    </button>
                    <HealthForm />
                  </div>
                </ProtectedRoute>
              } 
            />

            <Route 
              path="/doctors" 
              element={
                <ProtectedRoute isAuthenticated={isAuthenticated}>
                  <DoctorBooking />
                </ProtectedRoute>
              } 
            />

            <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;