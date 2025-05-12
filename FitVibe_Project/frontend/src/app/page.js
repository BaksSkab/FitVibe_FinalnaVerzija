import React from "react";
import Link from "next/link";
import "../styles/LandingPage.css"; // ispravno!

export default function Home() {
  return (
    <div className="landing-container">
      <nav className="navbar">
        <div className="logo">FitVibe</div>
        <div className="nav-buttons">
          <Link href="/login"><button className="btn">Login</button></Link>
          <Link href="/registration"><button className="btn">Registracija</button></Link>
        </div>
      </nav>

      <header className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Dobrodošli na FitVibe!</h1>
          <p className="hero-subtitle">Pridruži se i transformiši svoje fitness putovanje.</p>
          <Link href="/registration"><button className="btn cta-btn">Počni sada</button></Link>
        </div>
      </header>
    </div>
  );
}
