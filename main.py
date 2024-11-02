from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Employee as EmployeeModel
from schemas import EmployeeCreate, EmployeeUpdate, Employee  # Import Employee schema here
from auth import get_current_user, authenticate_user, create_access_token

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token")
def login_for_access_token(email: str, password: str, db: Session = Depends(get_db)):
    
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/employees/", response_model=Employee)  # Use Employee Pydantic model here
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    db_employee = EmployeeModel(name=employee.name, email=employee.email, department=employee.department, role=employee.role)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/api/employees/", response_model=list[Employee])  # Use list of Employee Pydantic model here
def get_employees(skip: int = 0, limit: int = 10, department: str = None, role: str = None, db: Session = Depends(get_db)):
    query = db.query(EmployeeModel)
    if department:
        query = query.filter(EmployeeModel.department == department)
    if role:
        query = query.filter(EmployeeModel.role == role)
    return query.offset(skip).limit(limit).all()

@app.get("/api/employees/{id}", response_model=Employee)  # Use Employee Pydantic model here
def get_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/api/employees/{id}", response_model=Employee)  # Use Employee Pydantic model here
def update_employee(id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee_update.dict(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

@app.delete("/api/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
