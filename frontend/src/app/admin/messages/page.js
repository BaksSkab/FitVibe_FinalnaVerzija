"use client";
import React, { useEffect, useState } from "react";
import "../admin.css";
import { useRouter } from "next/navigation";

export default function AdminMessagesPage() {
  const [messages, setMessages] = useState([]);
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [form, setForm] = useState({
    content: "",
    display_date: "",
  });
  const [editId, setEditId] = useState(null);
  
  
  const [notification, setNotification] = useState({ show: false, message: '', type: '' });

 
  const showNotification = (message, type = 'success') => {
    setNotification({ show: true, message, type });
    setTimeout(() => setNotification({ ...notification, show: false }), 3000);
  };

  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8001/admin/messages", {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri učitavanju poruka");
      }
      
      const data = await res.json();
      setMessages(data);
    } catch (error) {
      console.error("Greška pri učitavanju poruka:", error);
      showNotification("Došlo je do greške pri učitavanju poruka", 'error');
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
        ? `http://localhost:8001/admin/messages/${editId}`
        : "http://localhost:8001/admin/messages";

      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        throw new Error(res.statusText || "Greška prilikom snimanja poruke");
      }

      setForm({ content: "", display_date: "" });
      setEditId(null);
      fetchMessages();
      showNotification(`Poruka uspješno ${editId ? 'ažurirana' : 'dodana'}!`);
    } catch (error) {
      console.error("Greška:", error);
      showNotification(error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (msg) => {
    setForm({
      content: msg.content,
      display_date: msg.display_date,
    });
    setEditId(msg.id);
  };

  const handleDelete = async (id) => {
    if (!confirm("Da li želite obrisati ovu poruku?")) return;
    
    try {
      const res = await fetch(`http://localhost:8001/admin/messages/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error("Greška pri brisanju poruke");
      }

      fetchMessages();
      showNotification("Poruka uspješno obrisana!", 'delete');
    } catch (error) {
      console.error("Greška pri brisanju:", error);
      showNotification("Došlo je do greške pri brisanju poruke", 'error');
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

      <h1 className="admin-title">Motivacijske poruke</h1>

      <div className="admin-content">
        <form onSubmit={handleSubmit} className="admin-form">
          <h2>{editId ? "Uredi poruku" : "Dodaj novu poruku"}</h2>
          
          <div className="form-group">
            <label>Tekst poruke</label>
            <textarea
              placeholder="Unesite motivacijsku poruku..."
              value={form.content}
              onChange={(e) => setForm({ ...form, content: e.target.value })}
              required
              rows={5}
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label>Datum prikaza</label>
            <input
              type="date"
              value={form.display_date}
              onChange={(e) => setForm({ ...form, display_date: e.target.value })}
              required
              disabled={isLoading}
            />
          </div>

          <button 
            type="submit" 
            className="primary-btn"
            disabled={isLoading}
          >
            {isLoading ? (editId ? "Spremanje..." : "Dodavanje...") : (editId ? "Sačuvaj izmjene" : "Dodaj poruku")}
          </button>
        </form>

        <div className="messages-list">
          {isLoading ? (
            <div className="loading-spinner">Učitavanje poruka...</div>
          ) : messages.length > 0 ? (
            <div className="messages-grid">
              {messages.map((msg) => (
                <div key={msg.id} className="message-card">
                  <div className="message-content">
                    <p className="message-text">"{msg.content}"</p>
                    <p className="message-date">
                      {new Date(msg.display_date).toLocaleDateString('hr-HR')}
                    </p>
                  </div>
                  <div className="message-actions">
                    <button 
                      className="edit-btn"
                      onClick={() => handleEdit(msg)}
                      disabled={isLoading}
                    >
                      Uredi
                    </button>
                    <button 
                      className="delete-btn"
                      onClick={() => handleDelete(msg.id)}
                      disabled={isLoading}
                    >
                      Obriši
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              Trenutno nema dostupnih poruka
            </div>
          )}
        </div>
      </div>
    </div>
  );
}