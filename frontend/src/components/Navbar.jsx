import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Navbar({ onToggleSidebar, onToggleMobile, pageTitle = "Dashboard" }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();

  const adminName = localStorage.getItem("admin_name") || "Admin User";
  const initials = adminName
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <header className="navbar">
      <div className="navbar-left">
        <button className="navbar-toggle" onClick={onToggleSidebar} aria-label="Toggle sidebar">
          <i className="bi bi-list"></i>
        </button>
        <button className="navbar-burger" onClick={onToggleMobile} aria-label="Open menu">
          <i className="bi bi-list"></i>
        </button>
        <span className="navbar-title">{pageTitle}</span>
      </div>

      <div className="navbar-right">
        <button className="navbar-icon-btn" aria-label="Notifications">
          <i className="bi bi-bell"></i>
          <span className="badge-dot"></span>
        </button>

        <div className="navbar-user" ref={menuRef} style={{ position: "relative" }}>
          <div className="navbar-avatar">{initials || "AU"}</div>
          <div className="navbar-user-info">
            <div className="navbar-user-name">{adminName}</div>
            <div className="navbar-user-role">Administrator</div>
          </div>
          <button
            className="navbar-icon-btn"
            onClick={() => setMenuOpen((o) => !o)}
            aria-label="Account menu"
          >
            <i className="bi bi-chevron-down" style={{ fontSize: "0.8rem" }}></i>
          </button>

          {menuOpen && (
            <div
              className="card"
              style={{
                position: "absolute",
                right: 0,
                top: "calc(100% + 8px)",
                width: 180,
                padding: 8,
                zIndex: 950,
              }}
            >
              <button
                className="btn btn-outline w-full"
                style={{ justifyContent: "flex-start", border: "none" }}
                onClick={handleLogout}
              >
                <i className="bi bi-box-arrow-right"></i> Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}