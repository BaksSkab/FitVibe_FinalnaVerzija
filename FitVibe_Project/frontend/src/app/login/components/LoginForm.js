"use client";

import { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import "../login.css";

import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const LoginForm = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [showModal, setShowModal] = useState(false);
  const [resetData, setResetData] = useState({
    email: "",
    new_password: ""
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8001/auth/login", formData);

      Cookies.set("user_id", response.data.user_id || "");
      Cookies.set("trainer_id", response.data.trainer_id || "");
      Cookies.set("admin_id", response.data.admin_id || "");
      Cookies.set("first_name", response.data.first_name);
      localStorage.setItem("token", response.data.access_token);

      toast.success("Login uspješan!");

      setTimeout(() => {
        if (response.data.role === "trainer") {
          window.location.href = "/trainer";
        } else if (response.data.role === "user") {
          window.location.href = "/user";
        } else if (response.data.role === "admin") {
          window.location.href = "/admin";
        }
      }, 1000);
    } catch (err) {
      console.error(err.response?.data || err.message);
      toast.error("Login nije uspio! Provjerite email ili lozinku.");
    }
  };

  const handlePasswordReset = async () => {
    try {
      await axios.post("http://localhost:8001/auth/reset-password", resetData);
      toast.success("Password reset successfully!");
      setShowModal(false);
      setResetData({ email: "", new_password: "" });
    } catch (err) {
      toast.error(err.response?.data.detail || "Error resetting password.");
    }
  };

  return (
    <>
      <div className="login-wrapper">
        <div className="video-panel">
          <video autoPlay loop muted playsInline>
            <source src="/videos/fifthVideo.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="login-panel">
          <h2>Login</h2>
          <p>Enter your account details to enter our platform.</p>

          <input type="email" name="email" placeholder="Email" onChange={handleChange} />
          <input type="password" name="password" placeholder="Password" onChange={handleChange} />

          <div
            className="forgot"
            style={{ cursor: "pointer" }}
            onClick={() => setShowModal(true)}
          >
            Forgot password?
          </div>

          <button className="primary-btn" onClick={handleLogin}>Login</button>

          <div className="signup-link">
            Don’t have an account? <a href="/registration">Create an account</a>
          </div>
        </div>
      </div>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Reset Password</h3>
            <input
              type="email"
              placeholder="Your email"
              value={resetData.email}
              onChange={(e) => setResetData({ ...resetData, email: e.target.value })}
            />
            <input
              type="password"
              placeholder="New password"
              value={resetData.new_password}
              onChange={(e) => setResetData({ ...resetData, new_password: e.target.value })}
            />
            <button className="primary-btn" onClick={handlePasswordReset}>
              Submit
            </button>
            <button className="primary-btn" onClick={() => setShowModal(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      <ToastContainer position="top-right" autoClose={3000} pauseOnHover={false} />
    </>
  );
};

export default LoginForm;
