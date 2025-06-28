"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function AdminPage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token || role !== "admin") {
      router.push("/login");
    }
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Dobrodošli, Admin!</h1>
      <p>Ovdje možete upravljati korisnicima, planovima, vježbama itd.</p>
    </div>
  );
}
