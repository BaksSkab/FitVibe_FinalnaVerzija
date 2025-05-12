import { useState } from "react";
import axios from "axios";
import "../registration.css";

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
      setStep(2);
    } else {
      alert("Popuni email, šifru i odaberi ulogu.");
    }
  };

  const handleRegister = async () => {
    try {
      const endpoint =
        role === "trainer"
          ? "http://localhost:8000/auth/register/trainer"
          : "http://localhost:8000/auth/register/user";

      await axios.post(endpoint, formData);
      alert("Registracija uspješna!");
      window.location.href = "/login";
    } catch (err) {
      alert("Greška pri registraciji.");
    }
  };

  return (
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
            <input name="password" type="password" placeholder="Šifra" onChange={handleChange} />
            <select onChange={(e) => setRole(e.target.value)}>
              <option value="">Odaberi ulogu</option>
              <option value="user">Korisnik</option>
              <option value="trainer">Trener</option>
            </select>
            <button className="primary-btn" onClick={handleNext}>Dalje</button>
          </>
        )}

        {step === 2 && (
          <>
            <h2>Register</h2>
            <input name="first_name" placeholder="Ime" onChange={handleChange} />
            <input name="last_name" placeholder="Prezime" onChange={handleChange} />
            <input name="phone" placeholder="Telefon" onChange={handleChange} />
            {role === "user" && (
              <>
                <input name="goal" placeholder="Cilj" onChange={handleChange} />
                <select name="gender" onChange={handleChange}>
                  <option value="">Spol</option>
                  <option value="male">Muški</option>
                  <option value="female">Ženski</option>
                </select>
              </>
            )}
            <button className="primary-btn" onClick={handleRegister}>Register</button>
          </>
        )}
      </div>
    </div>
  );
};

export default RegistrationForm;
