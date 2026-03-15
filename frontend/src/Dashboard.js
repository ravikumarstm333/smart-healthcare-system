import React from "react";
import { useNavigate } from "react-router-dom";
import { ActivitySquare, CalendarHeart, LogOut } from "lucide-react";

function Dashboard({ onLogout }) {
  const navigate = useNavigate();
  const username = localStorage.getItem("username");

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem", width: "100%", maxWidth: "800px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid var(--glass-border)", paddingBottom: "1rem" }}>
        <h2>Overview, {username}</h2>
        <button 
          onClick={onLogout} 
          style={{ background: "transparent", border: "1px solid var(--glass-border)", color: "var(--text-muted)", padding: "0.5rem 1rem", borderRadius: "8px", display: "flex", alignItems: "center", gap: "0.5rem", cursor: "pointer", transition: "0.2s" }}
          onMouseOver={(e) => { e.currentTarget.style.color = "var(--danger)"; e.currentTarget.style.borderColor = "var(--danger)"}}
          onMouseOut={(e) => { e.currentTarget.style.color = "var(--text-muted)"; e.currentTarget.style.borderColor = "var(--glass-border)"}}
        >
          <LogOut size={16} /> Logout
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "1.5rem" }}>
        
        <div className="form-card" onClick={() => navigate("/predict")} style={{ cursor: "pointer", textAlign: "center", padding: "2rem" }}>
          <ActivitySquare size={48} color="var(--primary)" style={{ margin: "0 auto 1rem auto" }} />
          <h3 style={{ marginBottom: "0.5rem" }}>Health Analysis</h3>
          <p style={{ color: "var(--text-muted)", fontSize: "0.95rem" }}>Analyze your lifestyle and vitals to predict potential health risks.</p>
        </div>

        <div className="form-card" onClick={() => navigate("/doctors")} style={{ cursor: "pointer", textAlign: "center", padding: "2rem" }}>
          <CalendarHeart size={48} color="var(--accent)" style={{ margin: "0 auto 1rem auto" }} />
          <h3 style={{ marginBottom: "0.5rem" }}>Doctor Appointment Booking</h3>
          <p style={{ color: "var(--text-muted)", fontSize: "0.95rem" }}>Schedule a consultation with specialized medical professionals.</p>
        </div>

      </div>
    </div>
  );
}

export default Dashboard;
