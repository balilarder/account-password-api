from pydantic import BaseModel
from datetime import datetime

from typing import Optional

# class UserBase(BaseModel):
#     pass
#     # email: str


##
# class UserCreate(UserBase):
#     username: str
#     password: str

##
class UserCreate(BaseModel):
    username: str
    password: str



# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    fail_counter: int      # default 0
    lock_until: Optional[datetime] = None
    

    class Config:
        orm_mode = True