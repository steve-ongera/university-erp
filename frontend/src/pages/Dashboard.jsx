import React, { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import {
  getDashboardSummary,
  getEnrollmentTrend,
  getFeesByYear,
  getGradeDistribution,
} from "../services/api";

const PIE_COLORS = ["#2563eb", "#16a34a", "#d97706", "#dc2626", "#94a3b8"];

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [enrollment, setEnrollment] = useState([]);
  const [fees, setFees] = useState([]);
  const [grades, setGrades] = useState([]);

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(() => {});
    getEnrollmentTrend().then(setEnrollment).catch(() => {});
    getFeesByYear().then(setFees).catch(() => {});
    getGradeDistribution().then(setGrades).catch(() => {});
  }, []);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>Overview of students, fees, and academic performance.</p>
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-icon blue"><i className="bi bi-people"></i></div>
          <div>
            <div className="stat-value">{summary?.total_students ?? "—"}</div>
            <div className="stat-label">Total Students</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon green"><i className="bi bi-person-workspace"></i></div>
          <div>
            <div className="stat-value">{summary?.total_lecturers ?? "—"}</div>
            <div className="stat-label">Active Lecturers</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon amber"><i className="bi bi-mortarboard"></i></div>
          <div>
            <div className="stat-value">{summary?.total_programmes ?? "—"}</div>
            <div className="stat-label">Programmes</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon red"><i className="bi bi-graph-up-arrow"></i></div>
          <div>
            <div className="stat-value">{summary ? `${summary.pass_rate}%` : "—"}</div>
            <div className="stat-label">Overall Pass Rate</div>
          </div>
        </div>
      </div>

      <div className="chart-grid">
        <div className="card chart-card">
          <h3>Enrollment Trend</h3>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={enrollment}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="year" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Line type="monotone" dataKey="students" stroke="#2563eb" strokeWidth={2.5} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card chart-card">
          <h3>Grade Distribution</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={grades} dataKey="count" nameKey="grade" innerRadius={50} outerRadius={85} paddingAngle={3}>
                {grades.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Legend />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card chart-card">
        <h3>Fees Collected by Academic Year (KES)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={fees}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="year" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="collected" fill="#16a34a" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}