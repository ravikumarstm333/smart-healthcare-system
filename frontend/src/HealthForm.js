import React, { useState } from "react";
import axios from "axios";
import { User, Activity, HeartPulse, ActivitySquare, Pill, Flame, Droplets, Moon, Coffee, Cigarette, AlertTriangle, CheckCircle2, CalendarPlus } from "lucide-react";

function HealthForm() {
  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    bmi: "",
    daily_steps: "",
    sleep_hours: "",
    water_intake_l: "",
    calories_consumed: "",
    smoker: "",
    alcohol: "",
    resting_hr: "",
    systolic_bp: "",
    diastolic_bp: "",
    cholesterol: "",
    family_history: ""
  });

  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setResult("");
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", {
        age: Number(formData.age),
        gender: Number(formData.gender),
        bmi: Number(formData.bmi),
        daily_steps: Number(formData.daily_steps),
        sleep_hours: Number(formData.sleep_hours),
        water_intake_l: Number(formData.water_intake_l),
        calories_consumed: Number(formData.calories_consumed),
        smoker: Number(formData.smoker),
        alcohol: Number(formData.alcohol),
        resting_hr: Number(formData.resting_hr),
        systolic_bp: Number(formData.systolic_bp),
        diastolic_bp: Number(formData.diastolic_bp),
        cholesterol: Number(formData.cholesterol),
        family_history: Number(formData.family_history)
      });
      // Simulate slight delay for better UI feedback
      setTimeout(() => {
        setResult(res.data.risk);
        setIsLoading(false);
      }, 800);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the prediction server. Please try again.");
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        
        {/* Personal Details */}
        <div className="section-title">
          <User size={20} className="text-primary" />
          <h3>Personal Details</h3>
        </div>
        <div className="form-grid">
          <div className="input-group">
            <label>Age</label>
            <input name="age" type="number" required placeholder="e.g. 35" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Gender</label>
            <select name="gender" required onChange={handleChange}>
              <option value="">Select Gender</option>
              <option value="1">Male</option>
              <option value="0">Female</option>
            </select>
          </div>
          <div className="input-group">
            <label>BMI</label>
            <input name="bmi" type="number" step="0.1" required placeholder="e.g. 24.5" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Family History of Disease</label>
            <select name="family_history" required onChange={handleChange}>
              <option value="">Select Option</option>
              <option value="1">Yes</option>
              <option value="0">No</option>
            </select>
          </div>
        </div>

        {/* Lifestyle & Habits */}
        <div className="section-title">
          <ActivitySquare size={20} className="text-primary" />
          <h3>Lifestyle & Habits</h3>
        </div>
        <div className="form-grid">
          <div className="input-group">
            <label><Activity size={16} style={{display:'inline', marginRight:'4px'}}/>Daily Steps</label>
            <input name="daily_steps" type="number" required placeholder="e.g. 8000" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label><Moon size={16} style={{display:'inline', marginRight:'4px'}}/>Sleep (Hours)</label>
            <input name="sleep_hours" type="number" step="0.1" required placeholder="e.g. 7.5" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label><Droplets size={16} style={{display:'inline', marginRight:'4px'}}/>Water Intake (L)</label>
            <input name="water_intake_l" type="number" step="0.1" required placeholder="e.g. 2.5" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label><Flame size={16} style={{display:'inline', marginRight:'4px'}}/>Calories Consumed</label>
            <input name="calories_consumed" type="number" required placeholder="e.g. 2200" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label><Cigarette size={16} style={{display:'inline', marginRight:'4px'}}/>Smoker</label>
            <select name="smoker" required onChange={handleChange}>
              <option value="">Are you a smoker?</option>
              <option value="1">Yes</option>
              <option value="0">No</option>
            </select>
          </div>
          <div className="input-group">
            <label><Coffee size={16} style={{display:'inline', marginRight:'4px'}}/>Alcohol Consumption</label>
            <select name="alcohol" required onChange={handleChange}>
              <option value="">Do you consume alcohol?</option>
              <option value="1">Yes</option>
              <option value="0">No</option>
            </select>
          </div>
        </div>

        {/* Vitals */}
        <div className="section-title">
          <HeartPulse size={20} className="text-primary" />
          <h3>Health Vitals</h3>
        </div>
        <div className="form-grid">
          <div className="input-group">
            <label>Resting Heart Rate (bpm)</label>
            <input name="resting_hr" type="number" required placeholder="e.g. 72" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Systolic BP (mmHg)</label>
            <input name="systolic_bp" type="number" required placeholder="e.g. 120" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Diastolic BP (mmHg)</label>
            <input name="diastolic_bp" type="number" required placeholder="e.g. 80" onChange={handleChange} />
          </div>
          <div className="input-group">
            <label>Cholesterol Level (mg/dL)</label>
            <input name="cholesterol" type="number" required placeholder="e.g. 190" onChange={handleChange} />
          </div>
        </div>

        {error && <div style={{color: 'var(--danger)', marginTop: '1rem', textAlign: 'center'}}>{error}</div>}

        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? (
            <>
              <Activity className="spinner" size={20} />
              Analyzing Data...
            </>
          ) : (
            <>
              <Pill size={20} />
              Analyze Health Risk
            </>
          )}
        </button>
      </form>

      {result && (
        <div className={`result-card ${result === "High Risk" ? "high-risk" : "low-risk"}`}>
          <h2>AI Prediction Result</h2>
          {result === "High Risk" ? (
            <AlertTriangle size={48} color="var(--danger)" style={{ margin: "1rem auto" }} />
          ) : (
            <CheckCircle2 size={48} color="var(--success)" style={{ margin: "1rem auto" }} />
          )}
          <div className="risk-level">{result}</div>
          <p style={{ color: "var(--text-muted)" }}>
            {result === "High Risk" 
              ? "Warning: Your lifestyle and vitals indicate a higher risk map. We strongly recommend consulting a healthcare professional immediately." 
              : "Great! Your current lifestyle metrics indicate a lower risk profile. Keep up the good work!"}
          </p>

          {result === "High Risk" && (
            <button 
              className="submit-btn" 
              style={{ marginTop: "2rem", background: "var(--danger)", boxShadow: "0 10px 30px -10px var(--danger)" }}
              onClick={() => window.location.href = "/doctors"}
            >
              <CalendarPlus size={20} />
              Book Doctor Appointment Now
            </button>
          )}

        </div>
      )}
    </div>
  );
}

export default HealthForm;