<div align="center">

# 🏥 Healthcare Data Management System

A full-stack **Healthcare Data Management System** built using **FastAPI**, featuring **JWT-based authentication**, **role-based access control**, and a clean **HTML/CSS frontend** rendered using templates.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-red)
![Status](https://img.shields.io/badge/Status-Interview%20Ready-brightgreen)

</div>

---

## 🚀 Project Overview

The **Healthcare Data Management System** is a role-based web application designed to manage patient and medical records securely.  
It uses **FastAPI** for backend logic, **JWT authentication** for security, and **HTML/CSS templates** for the frontend UI.

This project demonstrates **real-world backend development**, authentication workflows, database handling, and server-side rendered pages.

---

## ✨ Features

- 🔐 JWT-based Login & Registration
- 👥 Role-Based Access Control (Admin / User)
- 🧾 Patient Management
- 🏥 Medical Records Management
- 🎨 HTML & CSS Frontend (Templates)
- ⚡ FastAPI-powered backend
- 📘 Auto-generated Swagger API Docs

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | FastAPI |
| Language | Python |
| Frontend | HTML, CSS |
| Database | MySQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Server | Uvicorn |

---

## 📂 Project Structure

```bash
Healthcare_app/
│
├── backend/
│   ├── __pycache__/
│   ├── auth.py              # Authentication & JWT logic
│   ├── config.py            # App & database configuration
│   ├── database.py          # Database connection
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── requirements.txt     # Project dependencies
│
├── static/
│   └── css/
│       └── style.css        # Application styling
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── patients.html
│   ├── patient_detail.html
│   ├── add_patient.html
│   └── add_medical_record.html
│
├── .gitignore
└── README.md


⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/healthcare-app.git
cd Healthcare_app/backend

2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Database
Update database credentials in config.py:
DATABASE_URL = "mysql+pymysql://username:password@localhost/database_name"


Make sure:

MySQL server is running
Database exists

5️⃣ Run the Application
uvicorn main:app --reload

🌐 Access the Application

🌍 Web App

http://127.0.0.1:8000


📘 Swagger API Docs

http://127.0.0.1:8000/docs


📕 ReDoc

http://127.0.0.1:8000/redoc

🔐 Authentication Flow
Register / Login → JWT Token → Protected Routes → Role Validation


JWT token is used internally to secure routes and sessions.

🧪 Key Functionalities
User Registration & Login
Add and View Patients
Add Medical Records
View Patient Details
Dashboard Overview
Secure Access Control

🎯 Why This Project Matters

✔ Demonstrates real-world FastAPI usage
✔ Secure authentication implementation
✔ Backend + frontend integration
✔ Interview-ready healthcare use case

This is not a basic CRUD app — it reflects industry-aligned backend design.

🚧 Future Enhancements
Doctor / Admin role separation
Appointment booking
File uploads (medical reports)
Docker support
Cloud deployment

👨‍💻 Author
Shobhit
Backend Developer | Python | FastAPI

📍 India
💻 Passionate about building secure and scalable applications
⭐ Support

If you like this project:
⭐ Star the repository
🍴 Fork it
🧠 Learn from it
🚀 Improve it

Clean code. Secure systems. Real backend energy.

