import React, { useState, useEffect } from "react";
import axios from "axios";
import { User, Stethoscope, Clock, CalendarCheck } from "lucide-react";

function DoctorBooking() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [bookingState, setBookingState] = useState({
    doctorId: null,
    selectedTime: "",
    selectedDate: ""
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/doctors");
        setDoctors(res.data);
      } catch (err) {
        console.error("Failed to load doctors", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDoctors();
  }, []);

  const handleBook = async (doctor) => {
    if (!bookingState.selectedDate || !bookingState.selectedTime) {
      setMessage("Please select a date and time");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/book_appointment", {
        username: localStorage.getItem("username") || "Guest",
        doctor_name: doctor.name,
        specialization: doctor.specialization,
        date: bookingState.selectedDate,
        time: bookingState.selectedTime
      });
      setMessage(`Successfully booked appointment with ${doctor.name} on ${bookingState.selectedDate} at ${bookingState.selectedTime}`);
      setBookingState({ doctorId: null, selectedTime: "", selectedDate: "" });
    } catch (err) {
      setMessage("Failed to book appointment");
    }
  };

  if (loading) return <div>Loading available doctors...</div>;

  return (
    <div style={{ width: "100%", maxWidth: "800px" }}>
      <button 
        onClick={() => window.location.href = "/dashboard"} 
        style={{ background: "transparent", color: "var(--primary)", border: "none", cursor: "pointer", marginBottom: "1.5rem", fontWeight: "600" }}
      >
        ← Back to Dashboard
      </button>

      <h2>Book a Doctor Appointment</h2>
      <p style={{ color: "var(--text-muted)", marginBottom: "2rem" }}>Select a specialist from our trusted network of medical professionals.</p>

      {message && (
        <div style={{ padding: "1rem", background: "rgba(16, 185, 129, 0.1)", color: "var(--success)", border: "1px solid var(--success)", borderRadius: "10px", marginBottom: "2rem", textAlign: "center" }}>
          <CalendarCheck size={20} style={{ display: "inline", marginBottom: "-4px", marginRight: "8px" }} />
          {message}
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
        {doctors.map((doc) => (
          <div key={doc.id} className="form-card" style={{ padding: "1.5rem", display: "flex", flexDirection: "column", gap: "1rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "1rem" }}>
              <div>
                <h3 style={{ fontSize: "1.3rem", color: "var(--text-main)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <User size={20} color="var(--primary)" /> {doc.name}
                </h3>
                <p style={{ color: "var(--text-muted)", marginTop: "0.25rem" }}>
                  <Stethoscope size={14} style={{ display: "inline", marginBottom: "-2px" }} /> {doc.specialization} &bull; {doc.hospital}
                </p>
              </div>
              
              <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                <input 
                  type="date" 
                  min={new Date().toISOString().split('T')[0]}
                  className="input-group" 
                  style={{ padding: "0.5rem", borderRadius: "8px", background: "var(--input-bg)", border: "1px solid var(--glass-border)", color: "var(--text-main)" }}
                  onChange={(e) => setBookingState({ ...bookingState, doctorId: doc.id, selectedDate: e.target.value })}
                />
                <select 
                  className="input-group"
                  style={{ padding: "0.5rem", borderRadius: "8px", background: "var(--input-bg)", border: "1px solid var(--glass-border)", color: "var(--text-main)" }}
                  onChange={(e) => setBookingState({ ...bookingState, doctorId: doc.id, selectedTime: e.target.value })}
                >
                  <option value="">Select Time</option>
                  {doc.available_times.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
                <button 
                  className="submit-btn" 
                  style={{ marginTop: 0, padding: "0.5rem 1rem", width: "auto" }}
                  onClick={() => handleBook(doc)}
                >
                  Book Slot
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DoctorBooking;
