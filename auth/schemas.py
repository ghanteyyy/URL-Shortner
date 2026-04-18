import uuid
from fastapi import Form
from datetime import date
from pydantic import BaseModel, EmailStr
from .models import GenderEnum



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    gender: GenderEnum
    dob: date

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
        gender: GenderEnum = Form(...),
        dob: date = Form(...),
    ):
        return cls(name=name, email=email, password=password, gender=gender, dob=dob)


class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    gender: GenderEnum

    class Config:
        from_attributes = True
