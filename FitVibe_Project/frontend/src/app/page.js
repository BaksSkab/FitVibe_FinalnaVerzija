"use client";
import React from "react";
import Link from "next/link";
import "../styles/LandingPage.css";

export default function Home() {
  return (
    <div className="landing-container">
      {}
      <video autoPlay loop muted playsInline className="background-video">
        <source src="/videos/landingVideo.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {}
      <nav className="navbar fade-in-down">
        <div className="logo">FitVibe</div>
        <div className="nav-buttons">
          <Link href="/login"><button className="btn">Login</button></Link>
          <Link href="/registration"><button className="btn">Registration</button></Link>
        </div>
      </nav>

      {}
      <header className="hero-section fade-in-up">
        <div className="hero-content">
          <h1 className="hero-title">Welcome on FitVibe!</h1>
          <p className="hero-subtitle">Join into our programs and become the best version of yourself!</p>
          <Link href="/registration">
            <button className="btn cta-btn fade-in-scale">One click change everything</button>
          </Link>
        </div>
      </header>
    </div>
  );
}
