from pydantic import BaseModel
from datetime import datetime

from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    fail_counter: int
    lock_until: Optional[datetime] = None
    
    class Config:
        orm_mode = True