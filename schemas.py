from pydantic import BaseModel, EmailStr
from datetime import date

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str | None = None
    role: str | None = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    date_joined: date

    class Config:
        from_attributes = True
