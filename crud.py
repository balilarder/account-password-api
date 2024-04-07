from sqlalchemy.orm import Session
from datetime import datetime, timedelta

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = salt_password(user.password)
    
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_fail_counter(db: Session, user: models.User, set_to: int):

    if set_to:
        user.fail_counter += 1

        if user.fail_counter >= 5:
            user.fail_counter = 0
            user.lock_until = datetime.now() + timedelta(minutes=1)
    else:
        user.fail_counter = 0
    
    db.commit()


def salt_password(password: str):
    return password + "notreallyhashed"