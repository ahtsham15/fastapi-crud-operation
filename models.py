from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean

from database import Base,engine

def create_tables():
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    isMale = Column(Boolean, nullable=False)
    
    
