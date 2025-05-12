"use client";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";

const AdminPage = () => {
  const [name, setName] = useState("");

  useEffect(() => {
    const storedName = Cookies.get("full_name");
    if (storedName) setName(storedName);
  }, []);

  const handleLogout = () => {
    Cookies.remove("full_name");
    Cookies.remove("admin_id");
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div>
      <h1>Dobro došao Admine, {name}</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminPage;
