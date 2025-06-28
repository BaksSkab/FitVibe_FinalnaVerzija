"use client";
import { useRouter } from "next/navigation";
import { useEffect } from 'react';
import "./admin.css";

export default function AdminPage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      
      router.push("/login");
    }
  }, []);

  return (
    <div className="admin-panel">
      <h1 className="admin-title">Administrator</h1>

      <div className="admin-grid-row">
        <div className="admin-grid-item" onClick={() => router.push("/admin/users")}>
           <span>Korisnici</span>
        </div>
        <div className="admin-grid-item" onClick={() => router.push("/admin/workouts")}>
           <span>Vježbe</span>
        </div>
      </div>

      <div className="admin-grid-row">
        <div className="admin-grid-item" onClick={() => router.push("/admin/challenges")}>
           <span>Izazovi</span>
        </div>
        <div className="admin-grid-item" onClick={() => router.push("/admin/messages")}>
           <span>Poruke</span>
        </div>
      </div>

      <button
        className="logout-btn"
        onClick={() => {
          localStorage.removeItem("token");
          router.push("/login");
        }}
      >
        Logout
      </button>
    </div>
  );
}
