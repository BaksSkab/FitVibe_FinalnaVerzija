"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import "../admin.css";

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [editForm, setEditForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    gender: "",
    goal: ""
  });
  const [isLoading, setIsLoading] = useState(false);

  const router = useRouter();
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const [notification, setNotification] = useState({ show: false, message: '', type: '' });


  const showNotification = (message, type = 'success') => {
    setNotification({ show: true, message, type });
    setTimeout(() => setNotification({ ...notification, show: false }), 3000);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8001/admin/users", {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri učitavanju korisnika");
      }
      
      const data = await res.json();
      setUsers(data);
    } catch (error) {
      console.error("Greška pri učitavanju korisnika:", error);
      showNotification("Došlo je do greške pri učitavanju korisnika", 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditClick = (user) => {
    setCurrentUser(user);
    setEditForm({
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      phone: user.phone,
      gender: user.gender || "",
      goal: user.goal || ""
    });
    setIsEditModalOpen(true);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const res = await fetch(`http://localhost:8001/admin/users/${currentUser.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(editForm),
      });

      if (!res.ok) {
        throw new Error("Greška pri ažuriranju korisnika");
      }

      setIsEditModalOpen(false);
      fetchUsers();
      showNotification("Korisnik uspješno ažuriran!");
    } catch (error) {
      console.error("Greška pri ažuriranju korisnika:", error);
      showNotification(error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Da li želite obrisati korisnika?")) return;
    
    try {
      const res = await fetch(`http://localhost:8001/admin/users/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri brisanju korisnika");
      }
      
      fetchUsers();
      showNotification("Korisnik uspješno obrisan!", 'delete');
    } catch (error) {
      console.error("Greška pri brisanju korisnika:", error);
      showNotification("Došlo je do greške pri brisanju korisnika", 'error');
    }
  };

  return (
    <div className="users-container">
      {notification.show && (
        <div className={`${notification.type}-alert`}>
          {notification.message}
        </div>
      )}
      
      <button className="btn btn-back" onClick={() => router.push("/admin")}>
        ⬅
      </button>
      
      <h1 className="users-header">Svi korisnici</h1>

      {isLoading ? (
        <div className="loading-spinner">Učitavanje korisnika...</div>
      ) : (
        <div className="user-list">
          {users.map((user) => (
            <div key={user.id} className="user-card">
              <div className="user-info">
                <p><strong>Ime:</strong> {user.first_name} {user.last_name}</p>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Telefon:</strong> {user.phone}</p>
                {user.gender && <p><strong>Spol:</strong> {user.gender}</p>}
                {user.goal && <p><strong>Cilj:</strong> {user.goal}</p>}
              </div>
              
              <div className="user-divider"></div>
              
              <div className="user-actions">
                <button 
                  className="btn btn-edit"
                  onClick={() => handleEditClick(user)}
                  disabled={isLoading}
                >
                  Uredi
                </button>
                <button 
                  className="btn btn-delete"
                  onClick={() => handleDelete(user.id)}
                  disabled={isLoading}
                >
                  Obriši
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {isEditModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Uredi korisnika</h2>
            <form onSubmit={handleEditSubmit} className="edit-form">
              <div className="form-group">
                <label>Ime</label>
                <input
                  type="text"
                  value={editForm.first_name}
                  onChange={(e) => setEditForm({...editForm, first_name: e.target.value})}
                  required
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label>Prezime</label>
                <input
                  type="text"
                  value={editForm.last_name}
                  onChange={(e) => setEditForm({...editForm, last_name: e.target.value})}
                  required
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={editForm.email}
                  onChange={(e) => setEditForm({...editForm, email: e.target.value})}
                  required
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label>Telefon</label>
                <input
                  type="text"
                  value={editForm.phone}
                  onChange={(e) => setEditForm({...editForm, phone: e.target.value})}
                  required
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label>Spol</label>
                <input
                  type="text"
                  value={editForm.gender}
                  onChange={(e) => setEditForm({...editForm, gender: e.target.value})}
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label>Cilj</label>
                <input
                  type="text"
                  value={editForm.goal}
                  onChange={(e) => setEditForm({...editForm, goal: e.target.value})}
                  disabled={isLoading}
                />
              </div>

              <div className="modal-actions">
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={isLoading}
                >
                  {isLoading ? "Spremanje..." : "Sačuvaj"}
                </button>
                <button 
                  type="button"
                  className="btn btn-delete"
                  onClick={() => setIsEditModalOpen(false)}
                  disabled={isLoading}
                >
                  Odustani
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}