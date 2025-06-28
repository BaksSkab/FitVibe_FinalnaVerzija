"use client";
import React, { useEffect, useState } from "react";
import "../admin.css";
import { useRouter } from "next/navigation";

export default function AdminWorkoutsPage() {
  const [workouts, setWorkouts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const [images] = useState([
    "ab_crunch.png", "bent_over_row.png", "burpee.png",
    "cable_biceps_curl.png", "cable_kickback.png", "cable_lateral_raise.png",
    "cable_triceps_pushdown.png", "cable_woodchopper.png", "cat_cow_stretch.png",
    "chest_press_machine.png", "donkey_kick.png", "downward_dog.png",
    "dumbbell_shoulder_press.png", "fire_hydrant.png", "glute_bridge.png",
    "glute_kickback_machine.png", "hip_abduction_machine_i.png", "hip_abduction_machine_o.png",
    "jump_squat.png", "lat_pulldown.png", "lateral_raise.png",
    "leg_extension_machine.png", "leg_press_machine.png", "leg_raise.png",
    "lunges.png", "mountain_climbers.png", "pec_deck.png",
    "plank.png", "pull_up_machine.png", "push_ups.png",
    "russian_twist.png", "seated_calf_raise_machine.png", "seated_leg_curl_machine.png",
    "smith_machine_squat.png", "squat.png", "standing_calf_raise_machine.png",
    "step_up.png", "wall_sit.png"
  ]);

  const [notification, setNotification] = useState({ show: false, message: '', type: '' });


const showNotification = (message, type = 'success') => {
  setNotification({ show: true, message, type });
  setTimeout(() => setNotification({ ...notification, show: false }), 3000);
};


  const [form, setForm] = useState({
    title: "",
    description: "",
    category_id: "",
    image_url: ""
  });
  const [editId, setEditId] = useState(null);

  const router = useRouter();
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    fetchWorkouts();
    fetchCategories();
  }, []);

  const fetchWorkouts = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8001/admin/workouts", {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri učitavanju vježbi");
      }
      
      const data = await res.json();
      setWorkouts(data);
    } catch (error) {
      console.error("Greška pri učitavanju vježbi:", error);
      alert("Došlo je do greške pri učitavanju vježbi");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const res = await fetch("http://localhost:8001/admin/categories", {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri učitavanju kategorija");
      }
      
      const data = await res.json();
      setCategories(data);
    } catch (error) {
      console.error("Greška pri učitavanju kategorija:", error);
      alert("Došlo je do greške pri učitavanju kategorija");
    }
  };

 const handleSubmit = async (e) => {
  e.preventDefault();
  setIsLoading(true);
  setFormErrors({});


  const validationErrors = {};
  if (!form.title.trim()) validationErrors.title = "Naziv je obavezan";
  if (!form.description.trim()) validationErrors.description = "Opis je obavezan";
  if (!form.category_id) validationErrors.category_id = "Kategorija je obavezna";
  if (!form.image_url) validationErrors.image_url = "Slika je obavezna";

  if (Object.keys(validationErrors).length > 0) {
    setIsLoading(false);
    setFormErrors(validationErrors);
    return;
  }

  try {
    const requestData = {
      title: form.title.trim(),
      description: form.description.trim(),
      category_id: Number(form.category_id),
      image_url: form.image_url,
      trainer_id: 1 
    };

    const url = editId 
      ? `http://localhost:8001/admin/workouts/${editId}`
      : "http://localhost:8001/admin/workouts";
    
    const res = await fetch(url, {
      method: editId ? "PUT" : "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(requestData),
    });

    const data = await res.json();

    if (!res.ok) {
   
      if (data.errors?.trainer_id) {
        throw new Error("Morate biti prijavljeni kao trener da biste dodali vježbu");
      }
      throw new Error(data.message || "Došlo je do greške");
    }

  
    setForm({ title: "", description: "", category_id: "", image_url: "" });
    setEditId(null);
    fetchWorkouts();
    showNotification(`Vježba uspješno ${editId ? 'ažurirana' : 'dodana'}!`);

  } catch (error) {
    console.error("Greška:", error);
    alert(error.message);
  } finally {
    setIsLoading(false);
  }
};

  const handleEdit = (workout) => {
    setForm({
      title: workout.title,
      description: workout.description,
      category_id: workout.category_id,
      image_url: workout.image_url
    });
    setEditId(workout.id);
    setFormErrors({});
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (!confirm("Da li ste sigurni da želite obrisati ovu vježbu?")) return;
    
    try {
      const res = await fetch(`http://localhost:8001/admin/workouts/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      
      if (!res.ok) {
        throw new Error("Greška pri brisanju vježbe");
      }
      
      fetchWorkouts();
      showNotification("Vježba uspješno obrisana!", 'delete');
    } catch (error) {
      console.error("Greška pri brisanju:", error);
      alert("Došlo je do greške pri brisanju vježbe");
    }
  };

  return (
    <div className="admin-workouts-container">
      {notification.show && (
        <div className={`${notification.type}-alert`}>
          {notification.message}
        </div>
      )}
      <button className="btn btn-back" onClick={() => router.push("/admin")}>
        ⬅
      </button>

      <h1 className="admin-title">Vježbe</h1>

      <div className="admin-workouts-content">
        <form onSubmit={handleSubmit} className="admin-form">
          <h2>{editId ? "Uredi vježbu" : "Dodaj novu vježbu"}</h2>
          
      
          {(Object.keys(formErrors).length > 0) && (
            <div className="error-container">
              {Object.entries(formErrors).map(([field, message]) => (
                <div key={field} className="error-message">
                  {message}
                </div>
              ))}
            </div>
          )}

          <div className={`form-group ${formErrors.title ? 'has-error' : ''}`}>
            <label>Naziv vježbe</label>
            <input
              placeholder="Unesite naziv vježbe"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              disabled={isLoading}
            />
          </div>
          
          <div className={`form-group ${formErrors.description ? 'has-error' : ''}`}>
            <label>Opis vježbe</label>
            <textarea
              placeholder="Unesite opis vježbe"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              disabled={isLoading}
            />
          </div>
          
          <div className={`form-group ${formErrors.category_id ? 'has-error' : ''}`}>
            <label>Kategorija</label>
            <select
              value={form.category_id}
              onChange={(e) => setForm({ ...form, category_id: e.target.value })}
              disabled={isLoading}
            >
              <option value="">Odaberi kategoriju</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>

          <div className={`form-group image-select-wrapper ${formErrors.image_url ? 'has-error' : ''}`}>
            <label>Odaberi sliku</label>
            <select
              value={form.image_url}
              onChange={(e) => setForm({ ...form, image_url: e.target.value })}
              disabled={isLoading}
            >
              <option value="">Odaberi sliku</option>
              {images.map((img) => (
                <option key={img} value={`/images/workouts/${img}`}>
                  {img.replace('.png', '').replace(/_/g, ' ')}
                </option>
              ))}
            </select>
          </div>

          {form.image_url && (
            <div className="image-preview-container">
              <img 
                src={form.image_url} 
                alt="Preview" 
                className="image-preview"
              />
            </div>
          )}

          <button 
            type="submit" 
            className="primary-btn"
            disabled={isLoading}
          >
            {isLoading ? "Učitavanje..." : (editId ? "Sačuvaj izmjene" : "Dodaj")}
          </button>
        </form>

       {isLoading ? (
  <div className="loading-spinner">Učitavanje vježbi...</div>
) : (
  <div className="workout-grid">
    {workouts.map((w) => (
      <div key={w.id} className="workout-card">
        <div className="workout-image-container">
          <img 
  src={w.image_url || '/images/workouts/default.png'} 
  alt={w.title}
  className="workout-image"
  onError={(e) => {
    e.target.onerror = null; 
    e.target.src = '/images/workouts/default.png';
    console.log('Fallback to default image');
  }}
/>
        </div>
        <div className="workout-card-content">
          <h3>{w.title}</h3>
          <p className="workout-description">{w.description}</p>
          <p className="category">
            <strong>Kategorija:</strong> {categories.find(c => c.id === w.category_id)?.name || "Nepoznato"}
          </p>
          <div className="workout-actions">
            <button 
              className="edit-btn"
              onClick={() => handleEdit(w)}
              disabled={isLoading}
            >
               Uredi
            </button>
            <button 
              className="delete-btn"
              onClick={() => handleDelete(w.id)}
              disabled={isLoading}
            >
               Obriši
            </button>
          </div>
        </div>
      </div>
    ))}
  </div>
)}
      </div>
    </div>
  );
}