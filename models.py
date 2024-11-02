from sqlalchemy import Column, Integer, String, Date
from database import Base
import datetime

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String, index=True, nullable=True)
    role = Column(String, index=True, nullable=True)
    date_joined = Column(Date, default=datetime.datetime.utcnow)
