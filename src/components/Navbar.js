import React, { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { FaWhatsapp, FaPhone, FaSms, FaBars, FaTimes } from "react-icons/fa";
import "../styles/Navbar.css";

function Navbar() {
  const phone = "256753670268";
  const whatsAppMessage = "Hello, I'm interested in your products.";
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/" onClick={closeMenu}>
          <img src="/images/logo.JPG" alt="Caroline Ways Ltd" />
        </Link>
      </div>

      <div className="navbar-toggle" onClick={toggleMenu}>
        {menuOpen ? <FaTimes /> : <FaBars />}
      </div>

      <ul className={`navbar-links ${menuOpen ? "active" : ""}`}>
        <li><NavLink to="/" exact="true" onClick={closeMenu}>Home</NavLink></li>
        <li><NavLink to="/products" onClick={closeMenu}>Products</NavLink></li>
        <li><NavLink to="/about" onClick={closeMenu}>About</NavLink></li>
        <li><NavLink to="/contact" onClick={closeMenu}>Contact</NavLink></li>
        <li><NavLink to="/faq" onClick={closeMenu}>FAQ</NavLink></li>
        <li><NavLink to="/privacypolicy" onClick={closeMenu}>Privacy</NavLink></li>

        <li>
          <a
            href={`https://wa.me/${phone}?text=${encodeURIComponent(whatsAppMessage)}`}
            target="_blank"
            rel="noopener noreferrer"
            title="Chat on WhatsApp"
            onClick={closeMenu}
          >
            <FaWhatsapp className="icon-contact" />
          </a>
        </li>
        <li>
          <a href={`sms:+${phone}`} title="Send SMS" onClick={closeMenu}>
            <FaSms className="icon-contact" />
          </a>
        </li>
        <li>
          <a href={`tel:+${phone}`} title="Call Now" onClick={closeMenu}>
            <FaPhone className="icon-contact" />
          </a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
