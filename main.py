from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import re
import datetime

from passwd import verify_password
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
    return JSONResponse(content={"success": True}, status_code=201)


# API 2: Verify Account and Password
@app.post("/login")
def verify_account(user: schemas.UserCreate, db: Session = Depends(get_db)) -> JSONResponse:
    
    db_user = crud.get_user_by_name(db, username=user.username)
    if not db_user:
        content = {
            "success": False,
            "reason": "The user not existed."
        }
        return JSONResponse(content=content, status_code=401)
    
    print(f"Compare time, {db_user.lock_until}, {datetime.datetime.now()}")
    if db_user.lock_until > datetime.datetime.now():
        content = {
            "success": False,
            "reason": "The user is being locked"
        }
        return JSONResponse(content=content, status_code=403)
    
    # compare the user.password == db_user.hashed_password
    if not verify_password(plain_password=user.password, hashed_password=db_user.hashed_password):
    
        crud.set_fail_counter(db, db_user, 1)
        
        content = {
            "success": False,
            "reason": "The password is not corrected."
        }
        return JSONResponse(content=content, status_code=401)
    else:
        crud.set_fail_counter(db, db_user, 0)
        return JSONResponse(content={"success": True})

# testing: for listing all users
@app.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
