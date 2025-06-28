"use client";

import Cookies from "js-cookie";
import { useEffect, useState } from "react";

const UserPage = () => {
  const [ime, setIme] = useState("");

  useEffect(() => {
    const storedIme = Cookies.get("first_name");
    if (storedIme) setIme(storedIme);
  }, []);

  const handleLogout = () => {
    Cookies.remove("user_id");
    Cookies.remove("trainer_id");
    Cookies.remove("first_name");
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div>
      <h1>Zdravo, {ime}</h1>
      <button onClick={handleLogout} className="primary-btn">
        Logout
      </button>
    </div>
  );
};

export default UserPage;
