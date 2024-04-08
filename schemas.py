from pydantic import BaseModel
from datetime import datetime

from typing import Optional

# Input
class UserCreate(BaseModel):
    username: str
    password: str

# Output
class User(BaseModel):
    id: int
    username: str
    fail_counter: int
    lock_until: Optional[datetime] = None
    
    class Config:
        orm_mode = True