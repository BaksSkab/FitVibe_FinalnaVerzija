"use client";
import React, { useEffect, useState } from "react";
import "../admin.css";
import { useRouter } from "next/navigation";

export default function AdminChallengesPage() {
  const [challenges, setChallenges] = useState([]);
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [form, setForm] = useState({
    name: "",
    description: "",
    duration_days: "",
  });
  const [editId, setEditId] = useState(null);
  
  // Notifikacije stanje
  const [notification, setNotification] = useState({ show: false, message: '', type: '' });

  // Funkcija za prikaz notifikacije
  const showNotification = (message, type = 'success') => {
    setNotification({ show: true, message, type });
    setTimeout(() => setNotification({ ...notification, show: false }), 3000);
  };

  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8001/admin/challenges", {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri učitavanju izazova");
      }
      
      const data = await res.json();
      setChallenges(data);
    } catch (error) {
      console.error("Greška pri učitavanju izazova:", error);
      showNotification("Došlo je do greške pri učitavanju izazova", 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const method = editId ? "PUT" : "POST";
      const url = editId
        ? `http://localhost:8001/admin/challenges/${editId}`
        : "http://localhost:8001/admin/challenges";

      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: form.name,
          description: form.description,
          duration_days: Number(form.duration_days),
        }),
      });

      if (!res.ok) {
        throw new Error(res.statusText || "Greška prilikom snimanja izazova");
      }

      setForm({ name: "", description: "", duration_days: "" });
      setEditId(null);
      fetchChallenges();
      showNotification(`Izazov uspješno ${editId ? 'ažuriran' : 'dodan'}!`);
    } catch (error) {
      console.error("Greška:", error);
      showNotification(error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (challenge) => {
    setForm({
      name: challenge.name,
      description: challenge.description,
      duration_days: challenge.duration_days,
    });
    setEditId(challenge.id);
  };

  const handleDelete = async (id) => {
    if (!confirm("Da li želite obrisati izazov?")) return;
    
    try {
      const res = await fetch(`http://localhost:8001/admin/challenges/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error("Greška pri brisanju izazova");
      }

      fetchChallenges();
      showNotification("Izazov uspješno obrisan!", 'delete');
    } catch (error) {
      console.error("Greška pri brisanju:", error);
      showNotification("Došlo je do greške pri brisanju izazova", 'error');
    }
  };

  return (
    <div className="admin-container">
      {notification.show && (
        <div className={`${notification.type}-alert`}>
          {notification.message}
        </div>
      )}

      <button className="btn btn-back" onClick={() => router.push("/admin")}>
        ⬅
      </button>

      <h1 className="admin-title">Izazovi</h1>

      <div className="admin-content">
        <form onSubmit={handleSubmit} className="admin-form">
          <h2>{editId ? "Uredi izazov" : "Dodaj novi izazov"}</h2>
          
          <div className="form-group">
            <label>Naziv izazova</label>
            <input
              type="text"
              placeholder="Naziv izazova"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label>Opis</label>
            <textarea
              placeholder="Opis"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label>Trajanje (dana)</label>
            <input
              type="number"
              placeholder="Trajanje (dana)"
              value={form.duration_days}
              onChange={(e) => setForm({ ...form, duration_days: e.target.value })}
              required
              disabled={isLoading}
            />
          </div>

          <button 
            type="submit" 
            className="primary-btn"
            disabled={isLoading}
          >
            {isLoading ? (editId ? "Spremanje..." : "Dodavanje...") : (editId ? "Sačuvaj izmjene" : "Dodaj izazov")}
          </button>
        </form>

        <div className="challenges-list">
          {isLoading ? (
            <div className="loading-spinner">Učitavanje izazova...</div>
          ) : challenges.length > 0 ? (
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Naziv</th>
                  <th>Opis</th>
                  <th>Trajanje</th>
                  <th>Akcije</th>
                </tr>
              </thead>
              <tbody>
                {challenges.map((ch) => (
                  <tr key={ch.id}>
                    <td>{ch.name}</td>
                    <td>{ch.description}</td>
                    <td>{ch.duration_days} dana</td>
                    <td className="actions-cell">
                      <button 
                        className="edit-btn"
                        onClick={() => handleEdit(ch)}
                        disabled={isLoading}
                      >
                        Uredi
                      </button>
                      <button 
                        className="delete-btn"
                        onClick={() => handleDelete(ch.id)}
                        disabled={isLoading}
                      >
                        Obriši
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              Trenutno nema dostupnih izazova
            </div>
          )}
        </div>
      </div>
    </div>
  );
}