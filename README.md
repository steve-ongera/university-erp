# University ERP System (Admin Module)

A full-stack University Enterprise Resource Planning system focused on the **Admin Module**. Built with Django REST Framework (backend) and React (frontend), this system allows administrators to manage students, lecturers, programmes, academic years, marks/results, fees, and view analytical dashboards.

---

##  Tech Stack

**Backend:** Django 5.x, Django REST Framework, SimpleJWT, PostgreSQL
**Frontend:** React (Vite), Axios, React Router, Recharts, Bootstrap Icons
**Auth:** JWT (access/refresh tokens)

---

##  Project Structure

```
university-erp/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   │
│   ├── university_erp/                 # main project config
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── core/                           # single core app
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       ├── filters.py
│       ├── seed.py                     # management command for seed data
│       └── migrations/
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    │
    ├── public/
    │
    └── src/
        ├── main.jsx
        ├── App.jsx                      # all routes defined here
        │
        ├── components/
        │   ├── Sidebar.jsx
        │   └── Navbar.jsx
        │
        ├── services/
        │   └── api.js                   # single axios instance + all API calls
        │
        ├── styles/
        │   └── main.css                 # global clean theme
        │
        └── pages/
            ├── Dashboard.jsx
            ├── Students.jsx
            ├── Lecturers.jsx
            ├── Programmes.jsx
            ├── AcademicYears.jsx
            ├── Marks.jsx
            ├── Fees.jsx
            └── Login.jsx
```

---

##  Core Models

| Model | Description |
|---|---|
| `AcademicYear` | e.g. 2025/2026, with current-year flag |
| `Semester` | Linked to AcademicYear |
| `Department` | Owns programmes |
| `Programme` | Degree/diploma programmes, linked to Department |
| `Lecturer` | Staff who teach courses |
| `Course` | Linked to Programme, taught by Lecturer |
| `Student` | Linked to Programme & AcademicYear |
| `Mark` | Student results per course/semester |
| `FeeStructure` | Defines fees per programme/year |
| `FeePayment` | Tracks payments made by students |

---

##  Key Features

- JWT authentication (admin login)
- Full CRUD for Students, Lecturers, Programmes, Academic Years, Courses
- Marks entry & grading (auto grade computation)
- Fees management (invoice balance, payments, M-Pesa-ready structure)
- Dashboard analytics:
  - Total students/lecturers/programmes
  - Enrollment trend per academic year
  - Fees collected vs outstanding
  - Pass/fail rate per course

---

##  Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

##  Environment Variables (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=university_erp
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```