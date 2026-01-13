from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
import auth
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# Setup templates
from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")


# Dependency to get current user from cookie
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    payload = auth.verify_token(token)
    if not payload:
        return None
    
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    return user

def require_auth(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user

# ============= PUBLIC ROUTES =============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user or not auth.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password"
        })
    
    access_token = auth.create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email already registered"
        })
    
    # Create new user
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=models.UserRole[role.upper()]
    )
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url="/login?registered=true", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    return response

# ============= PROTECTED ROUTES =============

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: models.User = Depends(require_auth)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": current_user
    })

@app.get("/patients", response_class=HTMLResponse)
async def list_patients(
    request: Request,
    current_user: models.User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    patients = db.query(models.Patient).all()
    return templates.TemplateResponse("patients.html", {
        "request": request,
        "user": current_user,
        "patients": patients
    })

@app.get("/patients/add", response_class=HTMLResponse)
async def add_patient_page(
    request: Request,
    current_user: models.User = Depends(require_auth)
):
    return templates.TemplateResponse("add_patient.html", {
        "request": request,
        "user": current_user
    })

@app.post("/patients/add")
async def add_patient(
    request: Request,
    patient_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    blood_type: str = Form(None),
    current_user: models.User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    # Check if patient_id exists
    existing = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if existing:
        return templates.TemplateResponse("add_patient.html", {
            "request": request,
            "user": current_user,
            "error": "Patient ID already exists"
        })
    
    # Create patient
    new_patient = models.Patient(
        patient_id=patient_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=datetime.strptime(date_of_birth, "%Y-%m-%d"),
        phone=phone,
        email=email,
        address=address,
        blood_type=blood_type if blood_type else None
    )
    db.add(new_patient)
    db.commit()
    
    return RedirectResponse(url="/patients?added=true", status_code=303)

@app.get("/patients/{patient_id}", response_class=HTMLResponse)
async def patient_detail(
    request: Request,
    patient_id: int,
    current_user: models.User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return templates.TemplateResponse("patient_detail.html", {
        "request": request,
        "user": current_user,
        "patient": patient
    })

@app.get("/medical-records/add/{patient_id}", response_class=HTMLResponse)
async def add_medical_record_page(
    request: Request,
    patient_id: int,
    current_user: models.User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return templates.TemplateResponse("add_medical_record.html", {
        "request": request,
        "user": current_user,
        "patient": patient
    })

@app.post("/medical-records/add/{patient_id}")
async def add_medical_record(
    patient_id: int,
    visit_date: str = Form(...),
    diagnosis: str = Form(...),
    treatment: str = Form(...),
    notes: str = Form(None),
    current_user: models.User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    new_record = models.MedicalRecord(
        patient_id=patient_id,
        doctor_id=current_user.id,
        visit_date=datetime.strptime(visit_date, "%Y-%m-%d"),
        diagnosis=diagnosis,
        treatment=treatment,
        notes=notes if notes else None
    )
    db.add(new_record)
    db.commit()
    
    return RedirectResponse(url=f"/patients/{patient_id}?record_added=true", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)