import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Students from "./pages/Students";
import Lecturers from "./pages/Lecturers";
import Programmes from "./pages/Programmes";
import AcademicYears from "./pages/AcademicYears";
import Courses from "./pages/Courses";
import Marks from "./pages/Marks";
import Fees from "./pages/Fees";

import "./styles/main.css";

const pageTitles = {
  "/": "Dashboard",
  "/students": "Students",
  "/lecturers": "Lecturers",
  "/programmes": "Programmes",
  "/courses": "Courses",
  "/academic-years": "Academic Years",
  "/marks": "Marks",
  "/fees": "Fees",
};

function isAuthenticated() {
  return !!localStorage.getItem("access_token");
}

function ProtectedRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" replace />;
}

function AdminLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  // Close mobile drawer whenever the route changes
  useEffect(() => {
    setMobileOpen(false);
  }, [location.pathname]);

  const pageTitle = pageTitles[location.pathname] || "Varsity ERP";

  return (
    <div className={`app-shell ${collapsed ? "collapsed" : ""}`}>
      <Sidebar
        collapsed={collapsed}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      <div className="main-area">
        <Navbar
          pageTitle={pageTitle}
          onToggleSidebar={() => setCollapsed((c) => !c)}
          onToggleMobile={() => setMobileOpen((o) => !o)}
        />

        <main className="page-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/students" element={<Students />} />
            <Route path="/lecturers" element={<Lecturers />} />
            <Route path="/programmes" element={<Programmes />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/academic-years" element={<AcademicYears />} />
            <Route path="/marks" element={<Marks />} />
            <Route path="/fees" element={<Fees />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <AdminLayout />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}