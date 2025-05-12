"use client";

import { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import "../login.css";



const LoginForm = () => {
  const [role, setRole] = useState("user");
  const [formData, setFormData] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/auth/login/${role}`, formData);
      
  
      Cookies.set("trainer_id", response.data.trainer_id);
      Cookies.set("first_name", response.data.first_name);
      localStorage.setItem("token", response.data.access_token);
  
      if (role === "trainer") {
        window.location.href = "/trainer";
      }
      else if(role=="user"){
        window.location.href="/user";
      }
      else if(role=="admin"){
        window.location.href="/admin";
      }
  
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert("Login nije uspio!");
    }
  };
  

  return (
    <div className="login-wrapper">
      <div className="image-panel">
  <img src="/images/gym2.jpg" alt="gym" />
</div>
      <div className="login-panel">
        <h2>Login</h2>
        <p>Enter your account details to enter our platform.</p>

        <input type="email" name="email" placeholder="Email" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} />
        <div className="forgot">Forgot password?</div>

        <select onChange={(e) => setRole(e.target.value)}>
  <option value="user">Korisnik</option>
  <option value="trainer">Trener</option>
  <option value="admin">Admin</option>
</select>

        <button className="primary-btn" onClick={handleLogin}>Login</button>

        <div className="signup-link">
          Don’t have an account? <a href="/register">Create an account</a>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
