"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";  // import router iz Next.js
import "./profile.css";

export default function UserProfilePage() {
  const router = useRouter();  // koristi router

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    gender: "",
    goal: "",
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("http://localhost:8000/user/profile", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setForm(data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const res = await fetch("http://localhost:8000/user/profile", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(form),
    });

    if (res.ok) {
      alert("Profile updated!");
    } else {
      alert("Error updating profile.");
    }
  };

  return (
    <div className="profile-container">
      <h2>Edit Your Profile</h2>
      
      {/* Dugme za povratak nazad */}
      <button className="back-button" onClick={() => router.back()}>
        ← Back
      </button>

      <form onSubmit={handleSubmit} className="profile-form">
        <input
          type="text"
          placeholder="First Name"
          value={form.first_name}
          onChange={(e) => setForm({ ...form, first_name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Last Name"
          value={form.last_name}
          onChange={(e) => setForm({ ...form, last_name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Phone"
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />
        <input
          type="text"
          placeholder="Gender"
          value={form.gender}
          onChange={(e) => setForm({ ...form, gender: e.target.value })}
        />
        <input
          type="text"
          placeholder="Goal"
          value={form.goal}
          onChange={(e) => setForm({ ...form, goal: e.target.value })}
        />
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
}
