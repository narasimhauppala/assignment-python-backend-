from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Employee

# Initialize the database
Base.metadata.create_all(bind=engine)

# Define the test employee
def create_test_employee():
    db: Session = SessionLocal()
    try:
        test_employee = Employee(
            name="Test User",
            email="di@email.com",
            department="Engineering",
            role="Developer",
            password="12345"
        )
        db.add(test_employee)
        db.commit()
        db.refresh(test_employee)
        print("Test employee created:", test_employee.email)
    except Exception as e:
        print("Error creating test employee:", e)
    finally:
        db.close()

if __name__ == "__main__":
    create_test_employee()
