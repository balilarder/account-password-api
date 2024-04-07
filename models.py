from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)

    fail_counter = Column(Integer, default=0)
    
    # Error
    # lock_until = Column(DateTime, default=(func.now() + timedelta(hours=8)))
    
    # Workaround
    lock_until = Column(DateTime, default=datetime.now())