import React from "react";
import { NavLink } from "react-router-dom";

const navItems = [
  { section: "Overview", links: [{ to: "/", label: "Dashboard", icon: "bi-speedometer2" }] },
  {
    section: "Academics",
    links: [
      { to: "/academic-years", label: "Academic Years", icon: "bi-calendar3" },
      { to: "/programmes", label: "Programmes", icon: "bi-mortarboard" },
      { to: "/courses", label: "Courses", icon: "bi-journal-bookmark" },
    ],
  },
  {
    section: "People",
    links: [
      { to: "/students", label: "Students", icon: "bi-people" },
      { to: "/lecturers", label: "Lecturers", icon: "bi-person-workspace" },
    ],
  },
  {
    section: "Records",
    links: [
      { to: "/marks", label: "Marks", icon: "bi-clipboard-data" },
      { to: "/fees", label: "Fees", icon: "bi-cash-coin" },
    ],
  },
];

export default function Sidebar({ collapsed, mobileOpen, onCloseMobile }) {
  return (
    <>
      <aside
        className={`sidebar ${collapsed ? "collapsed" : ""} ${mobileOpen ? "mobile-open" : ""}`}
      >
        <div className="sidebar-brand">
          <i className="bi bi-bank2"></i>
          {!collapsed && <span>Varsity ERP</span>}
        </div>

        <nav className="sidebar-nav">
          {navItems.map((group) => (
            <div key={group.section}>
              {!collapsed && <div className="sidebar-section-label">{group.section}</div>}
              {group.links.map((link) => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  end={link.to === "/"}
                  className={({ isActive }) =>
                    `sidebar-link ${isActive ? "active" : ""}`
                  }
                  onClick={onCloseMobile}
                >
                  <i className={`bi ${link.icon}`}></i>
                  {!collapsed && <span>{link.label}</span>}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        {!collapsed && (
          <div className="sidebar-footer">
            <i className="bi bi-shield-check"></i> Admin Module v1.0
          </div>
        )}
      </aside>

      <div
        className={`sidebar-overlay ${mobileOpen ? "show" : ""}`}
        onClick={onCloseMobile}
      ></div>
    </>
  );
}