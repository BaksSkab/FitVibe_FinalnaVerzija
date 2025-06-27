"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import "./user.css";
import { toast } from "react-toastify";

export default function UserPage() {
  const [user, setUser] = useState(null);
  const [plans, setPlans] = useState([]);
  const [motivation, setMotivation] = useState("");
  const [subscribedPlanIds, setSubscribedPlanIds] = useState([]);
  const [myPlans, setMyPlans] = useState([]);
  const [progress, setProgress] = useState([]);

  // Novi state za prikaz detalja plana
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [showPlanDetails, setShowPlanDetails] = useState(false);

  const router = useRouter();
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [
        userRes,
        plansRes,
        myPlansRes,
        motivationRes,
        progressRes,
      ] = await Promise.all([
        fetch("http://localhost:8000/user/profile", { headers: { Authorization: `Bearer ${token}` } }),
        fetch("http://localhost:8000/user/plans", { headers: { Authorization: `Bearer ${token}` } }),
        fetch("http://localhost:8000/user/my-plans", { headers: { Authorization: `Bearer ${token}` } }),
        fetch("http://localhost:8000/user/motivational-message", { headers: { Authorization: `Bearer ${token}` } }),
        fetch("http://localhost:8000/user/my-progress", { headers: { Authorization: `Bearer ${token}` } }),
      ]);

      const userData = await userRes.json();
      const plansData = await plansRes.json();
      const myPlansData = await myPlansRes.json();
      const motivationData = await motivationRes.json();
      const progressData = await progressRes.json();

      setUser(userData);
      setPlans(plansData);
      setMyPlans(myPlansData);
      setMotivation(motivationData?.content || "Stay focused and keep pushing!");
      setSubscribedPlanIds(myPlansData.map(p => p.trainer_plan.id));
      setProgress(progressData);
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  const subscribe = async (planId) => {
    try {
      const res = await fetch(`http://localhost:8000/user/plans/${planId}/subscribe`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        toast.success("Successfully subscribed!");
        setSubscribedPlanIds(prev => [...prev, planId]);
        fetchData();
      } else {
        toast.error("Subscription failed");
      }
    } catch (error) {
      toast.error("Server error");
    }
  };

  const handleUnsubscribe = async (planId) => {
    try {
      const res = await fetch(`http://localhost:8000/user/my-plans/${planId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        toast.success("Successfully unsubscribed!");
        setMyPlans(prev => prev.filter(p => p.trainer_plan.id !== planId));
        setSubscribedPlanIds(prev => prev.filter(id => id !== planId));
      } else {
        toast.error("Unsubscribe failed");
      }
    } catch (error) {
      toast.error("Server error");
    }
  };

  // Dohvat detalja pojedinog plana
  const showPlanDetailsHandler = async (planId) => {
    try {
      const res = await fetch(`http://localhost:8000/user/plans/${planId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) {
        toast.error("Failed to load plan details");
        return;
      }
      const data = await res.json();
      setSelectedPlan(data);
      setShowPlanDetails(true);
    } catch (error) {
      toast.error("Server error");
    }
  };

  const handleEditProfile = () => {
    router.push("/user/profile");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    document.cookie = "user_id=; Max-Age=0";
    document.cookie = "trainer_id=; Max-Age=0";
    document.cookie = "admin_id=; Max-Age=0";
    document.cookie = "first_name=; Max-Age=0";
    router.push("/login");
  };

  // Prikaz detalja plana (koristi polja iz selectedPlan.trainer_plan)
  if (showPlanDetails && selectedPlan) {
  const plan = selectedPlan.trainer_plan;
  return (
    <div className="plan-detail-container">
      <button
        onClick={() => {
          setShowPlanDetails(false);
          setSelectedPlan(null);
        }}
        className="edit-button"
      >
        ← Back to plans
      </button>
      <h2>{plan.plan_name}</h2>
      <p>{plan.description}</p>
      <p><strong>Level:</strong> {plan.level}</p>
      <p><strong>Goal:</strong> {plan.goal}</p>
      <p><strong>Trainer:</strong> {plan.trainer ? `${plan.trainer.first_name} ${plan.trainer.last_name}` : "Unknown"}</p>
      <h3>Workouts:</h3>
      {plan.workouts && plan.workouts.length > 0 ? (
        <ul>
          {plan.workouts.map(w => (
            <li key={w.id}>
              <strong>{w.title}</strong> - {w.description} ({w.repetitions} reps)
            </li>
          ))}
        </ul>
      ) : (
        <p>No workouts assigned to this plan.</p>
      )}
    </div>
  );
}

  // Standardni prikaz liste korisnika i planova
  return (
    <div className="user-container">
      <div className="user-header">
        <h1>Welcome, {user?.first_name || "User"}!</h1>
        <div className="header-buttons">
          <button className="edit-button" onClick={handleEditProfile}>Edit Profile</button>
          <button className="edit-button" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      {motivation && <div className="motivation-box">💬 {motivation} 💪</div>}

      {/* Subscribed Plans */}
      <section className="user-section">
        <h2>📋 Your Subscribed Plans</h2>
        <div className="plan-grid">
          {myPlans.map(plan => plan.trainer_plan ? (
            <div
              key={plan.id}
              className="plan-card"
              style={{ cursor: "pointer" }}
              onClick={() => showPlanDetailsHandler(plan.trainer_plan.id)}
            >
              <h3>{plan.trainer_plan.plan_name}</h3>
              <p>{plan.trainer_plan.description}</p>
              <p><strong>Level:</strong> {plan.trainer_plan.level}</p>
              <p><strong>Goal:</strong> {plan.trainer_plan.goal}</p>
              <p><strong>Trainer:</strong> {
                plan.trainer_plan.trainer
                  ? `${plan.trainer_plan.trainer.first_name} ${plan.trainer_plan.trainer.last_name}`
                  : "Unknown"
              }</p>
              <button
                className="edit-button unsubscribe-button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleUnsubscribe(plan.trainer_plan.id);
                }}
              >
                Unsubscribe
              </button>
            </div>
          ) : null)}
        </div>
      </section>

      {/* Available Plans */}
      <section className="user-section">
        <h2>Available Plans</h2>
        <div className="plan-grid">
          {plans.map(plan => (
            <div key={plan.id} className="plan-card">
              <h3>{plan.plan_name}</h3>
              <p>{plan.description}</p>
              {subscribedPlanIds.includes(plan.id) ? (
                <button className="subscribed" disabled>✓ Subscribed</button>
              ) : (
                <button className="subscribe-button" onClick={() => subscribe(plan.id)}>Subscribe</button>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
