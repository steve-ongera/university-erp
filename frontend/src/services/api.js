import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ---- Attach JWT token to every request ----
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ---- Auto-refresh token on 401 ----
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        try {
          const { data } = await axios.post(`${BASE_URL}/auth/refresh/`, {
            refresh,
          });
          localStorage.setItem("access_token", data.access);
          originalRequest.headers.Authorization = `Bearer ${data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.clear();
          window.location.href = "/login";
        }
      } else {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Helper to unwrap DRF pagination ({count, next, previous, results}) into plain arrays
const unwrap = (data) => (data && Array.isArray(data.results) ? data.results : data);

/* ---------------- AUTH ---------------- */
export const login = (username, password) =>
  api.post("/auth/login/", { username, password });

/* ---------------- ACADEMIC YEARS ---------------- */
export const getAcademicYears = (params) =>
  api.get("/academic-years/", { params }).then((r) => unwrap(r.data));
export const getAcademicYear = (id) => api.get(`/academic-years/${id}/`);
export const createAcademicYear = (payload) => api.post("/academic-years/", payload);
export const updateAcademicYear = (id, payload) => api.put(`/academic-years/${id}/`, payload);
export const deleteAcademicYear = (id) => api.delete(`/academic-years/${id}/`);

/* ---------------- SEMESTERS ---------------- */
export const getSemesters = (params) =>
  api.get("/semesters/", { params }).then((r) => unwrap(r.data));
export const createSemester = (payload) => api.post("/semesters/", payload);
export const updateSemester = (id, payload) => api.put(`/semesters/${id}/`, payload);
export const deleteSemester = (id) => api.delete(`/semesters/${id}/`);

/* ---------------- DEPARTMENTS ---------------- */
export const getDepartments = (params) =>
  api.get("/departments/", { params }).then((r) => unwrap(r.data));
export const createDepartment = (payload) => api.post("/departments/", payload);
export const updateDepartment = (id, payload) => api.put(`/departments/${id}/`, payload);
export const deleteDepartment = (id) => api.delete(`/departments/${id}/`);

/* ---------------- PROGRAMMES ---------------- */
export const getProgrammes = (params) =>
  api.get("/programmes/", { params }).then((r) => unwrap(r.data));
export const createProgramme = (payload) => api.post("/programmes/", payload);
export const updateProgramme = (id, payload) => api.put(`/programmes/${id}/`, payload);
export const deleteProgramme = (id) => api.delete(`/programmes/${id}/`);

/* ---------------- LECTURERS ---------------- */
export const getLecturers = (params) =>
  api.get("/lecturers/", { params }).then((r) => unwrap(r.data));
export const createLecturer = (payload) => api.post("/lecturers/", payload);
export const updateLecturer = (id, payload) => api.put(`/lecturers/${id}/`, payload);
export const deleteLecturer = (id) => api.delete(`/lecturers/${id}/`);

/* ---------------- COURSES ---------------- */
export const getCourses = (params) =>
  api.get("/courses/", { params }).then((r) => unwrap(r.data));
export const createCourse = (payload) => api.post("/courses/", payload);
export const updateCourse = (id, payload) => api.put(`/courses/${id}/`, payload);
export const deleteCourse = (id) => api.delete(`/courses/${id}/`);

/* ---------------- STUDENTS ---------------- */
export const getStudents = (params) =>
  api.get("/students/", { params }).then((r) => unwrap(r.data));
export const getStudent = (id) => api.get(`/students/${id}/`);
export const createStudent = (payload) => api.post("/students/", payload);
export const updateStudent = (id, payload) => api.put(`/students/${id}/`, payload);
export const deleteStudent = (id) => api.delete(`/students/${id}/`);

/* ---------------- MARKS ---------------- */
export const getMarks = (params) =>
  api.get("/marks/", { params }).then((r) => unwrap(r.data));
export const createMark = (payload) => api.post("/marks/", payload);
export const updateMark = (id, payload) => api.put(`/marks/${id}/`, payload);
export const deleteMark = (id) => api.delete(`/marks/${id}/`);
export const bulkCreateMarks = (payload) => api.post("/marks/bulk_create/", payload);

/* ---------------- FEES ---------------- */
export const getFeeStructures = (params) =>
  api.get("/fee-structures/", { params }).then((r) => unwrap(r.data));
export const createFeeStructure = (payload) => api.post("/fee-structures/", payload);
export const updateFeeStructure = (id, payload) => api.put(`/fee-structures/${id}/`, payload);
export const deleteFeeStructure = (id) => api.delete(`/fee-structures/${id}/`);

export const getFeePayments = (params) =>
  api.get("/fee-payments/", { params }).then((r) => unwrap(r.data));
export const createFeePayment = (payload) => api.post("/fee-payments/", payload);
export const deleteFeePayment = (id) => api.delete(`/fee-payments/${id}/`);

/* ---------------- DASHBOARD ---------------- */
export const getDashboardSummary = () => api.get("/dashboard/summary/").then((r) => r.data);
export const getEnrollmentTrend = () => api.get("/dashboard/enrollment_trend/").then((r) => r.data);
export const getStudentsPerProgramme = () =>
  api.get("/dashboard/students_per_programme/").then((r) => r.data);
export const getFeesByYear = () => api.get("/dashboard/fees_by_year/").then((r) => r.data);
export const getGradeDistribution = () =>
  api.get("/dashboard/grade_distribution/").then((r) => r.data);
export const getGenderDistribution = () =>
  api.get("/dashboard/gender_distribution/").then((r) => r.data);

export default api;