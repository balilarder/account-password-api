from typing import Union

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import re

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# def read_root():
#     return {"hello": "World"}


# Validation input
class Validation:

    @staticmethod
    def check_username_valid(username: str) -> bool : 
        if len(username) >= 3 and len(username) <= 32:
            return True
        return False
    
    @staticmethod
    def check_password_valid(password: str) -> bool:
        re_digit_check = re.compile('\d')
        re_upper_check = re.compile('[A-Z]')
        re_lower_check = re.compile('[a-z]')
        if re_digit_check.search(password) and re_upper_check.search(password) and re_lower_check.search(password):
            if len(password) >= 8 and len(password) <= 32:
                return True
        return False
        


# API 1: Create Account
@app.post("/user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> JSONResponse:
    
    db_user = crud.get_user_by_name(db, username=user.username)
    
    if db_user:
        content = {
            "success": False,
            "reason": "Username already existed"
        }
        return JSONResponse(content=content, status_code=409)
    
    # check username ok
    if not Validation.check_username_valid(user.username):
        content = {
            "success": False,
            "reason": "Username length minimum is 3, and maximun is 32."
        }
        return JSONResponse(content=content, status_code=422)
        
    
    # check password ok
    if not Validation.check_password_valid(user.password):
       
        content = {
            "success": False,
            "reason": "Password length minimum is 8, and maximun is 32, with at least 1 uppercase, 1 lowercase, 1 number."
        }
        return JSONResponse(content=content, status_code=422)
    
    crud.create_user(db=db, user=user)
    return JSONResponse(content={"success": True})


# API 2: Verify Account and Password
# ...

@app.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    
    for user in users:
        print(f"user: {user}")
    
    print("here")
    return users
