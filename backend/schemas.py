from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PatientCreate(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    phone: str
    email: EmailStr
    address: str
    blood_type: Optional[str] = None

class MedicalRecordCreate(BaseModel):
    patient_id: int
    visit_date: str
    diagnosis: str
    treatment: str
    notes: Optional[str] = None