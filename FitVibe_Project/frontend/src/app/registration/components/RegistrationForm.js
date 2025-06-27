"use client";

import { useState } from "react";
import axios from "axios";
import "../registration.css";

import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const RegistrationForm = () => {
  const [step, setStep] = useState(1);
  const [role, setRole] = useState("");

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone: "",
    goal: "",
    gender: ""
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleNext = () => {
    if (role && formData.email && formData.password) {
      toast.success("The first step is already done, we go to the next one!");
      setStep(2);
    } else {
      toast.error("You must enter email, password and role!");
    }
  };

  const handleRegister = async () => {
    try {
      const endpoint =
        role === "trainer"
          ? "http://localhost:8001/auth/register/trainer"
          : "http://localhost:8001/auth/register/user";

      await axios.post(endpoint, formData);

      toast.success("Registration completed! You can login now.");

      setTimeout(() => {
        window.location.href = "/login";
      }, 2500);
    } catch (err) {
      toast.error("Error during registration.");
    }
  };

  return (
    <>
      <div className="registration-wrapper">
        <div className="left-panel">
          <h1>Join the FitVibe Experience</h1>
          <p>Stay motivated, track progress, and achieve your fitness goals.</p>
        </div>
        <div className="form-panel">
          {step === 1 && (
            <>
              <h2>Register</h2>
              <input name="email" type="email" placeholder="Email" onChange={handleChange} />
              <input name="password" type="password" placeholder="Password" onChange={handleChange} />
              <select onChange={(e) => setRole(e.target.value)}>
                <option value="">Choose role</option>
                <option value="user">User</option>
                <option value="trainer">Trainer</option>
              </select>
              <button className="primary-btn" onClick={handleNext}>Next</button>
            </>
          )}

          {step === 2 && (
            <>
              <h2>Register</h2>
              <input name="first_name" placeholder="First Name" onChange={handleChange} />
              <input name="last_name" placeholder="Last Name" onChange={handleChange} />
              <input name="phone" placeholder="Phone" onChange={handleChange} />
              {role === "user" && (
                <>
                  <input name="goal" placeholder="Goal (Optional)" onChange={handleChange} />
                  <select name="gender" onChange={handleChange}>
                    <option value="">Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </>
              )}
              <button className="primary-btn" onClick={handleRegister}>Register</button>
            </>
          )}
        </div>
      </div>
      <ToastContainer position="top-right" autoClose={3000} pauseOnHover={false} />
    </>
  );
};

export default RegistrationForm;
