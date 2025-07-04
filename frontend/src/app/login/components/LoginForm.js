"use client";

import { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import "../login.css";

import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const LoginForm = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });

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

      toast.success("Login successful !");

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
      toast.error("Login failed! Provjerite email ili lozinku.");
    }
  };

  return (
    <>
      <div className="login-wrapper">
        <div className="video-panel fade-slide-up">
          <video autoPlay loop muted playsInline>
            <source src="/videos/fifthVideo.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="login-panel fade-slide-right">
          <h2 className="fade-slide-up">Login</h2>
          <p className="fade-slide-up">Enter your account details to enter our platform.</p>

          <input className="fade-slide-right" type="email" name="email" placeholder="Email" onChange={handleChange} />
          <input className="fade-slide-right" type="password" name="password" placeholder="Password" onChange={handleChange} />
          <div className="forgot fade-slide-up">Forgot password?</div>

          <button className="primary-btn fade-slide-left" onClick={handleLogin}>Login</button>

          <div className="signup-link fade-slide-up">
            Don’t have an account? <a href="/registration">Create an account</a>
          </div>
        </div>
      </div>
      <ToastContainer position="top-right" autoClose={3000} pauseOnHover={false} />
    </>
  );
};

export default LoginForm;
