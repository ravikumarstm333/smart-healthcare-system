import React, { useState } from "react";
import axios from "axios";
import { LogIn, UserPlus, Lock, User } from "lucide-react";

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        const res = await axios.post("http://127.0.0.1:8000/login", formData);
        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("username", res.data.username);
        onLogin();
      } else {
        await axios.post("http://127.0.0.1:8000/register", formData);
        setIsLogin(true);
        setError("Registration successful! Please log in.");
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || "An error occurred. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
      <div className="form-card" style={{ maxWidth: "400px", padding: "2rem" }}>
        <h2 style={{ textAlign: "center", marginBottom: "1.5rem" }}>
          {isLogin ? "Welcome Back" : "Create Account"}
        </h2>
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <div className="input-group">
            <label><User size={16} style={{display:'inline', marginRight:'4px'}}/>Username</label>
            <input
              type="text"
              name="username"
              placeholder="Enter username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="input-group">
            <label><Lock size={16} style={{display:'inline', marginRight:'4px'}}/>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          {error && (
            <div style={{ color: error.includes("successful") ? "var(--success)" : "var(--danger)", fontSize: "0.9rem", textAlign: "center" }}>
              {error}
            </div>
          )}
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              "Please wait..."
            ) : isLogin ? (
              <><LogIn size={20} /> Log In</>
            ) : (
              <><UserPlus size={20} /> Register</>
            )}
          </button>
        </form>
        <div style={{ textAlign: "center", marginTop: "1.5rem", color: "var(--text-muted)", fontSize: "0.9rem" }}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <span
            style={{ color: "var(--primary)", cursor: "pointer", fontWeight: "600" }}
            onClick={() => {
              setIsLogin(!isLogin);
              setError("");
            }}
          >
            {isLogin ? "Register here" : "Log in here"}
          </span>
        </div>
      </div>
    </div>
  );
}

export default Auth;
