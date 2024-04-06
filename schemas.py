from pydantic import BaseModel

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
    # is_active: bool
    # items: list[Item] = []
    username: str
    hashed_password: str
    

    class Config:
        orm_mode = True