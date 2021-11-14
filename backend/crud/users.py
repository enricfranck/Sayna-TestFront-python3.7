from datetime import datetime
from typing import Any, Dict, List, Union
from core.hashing import Hasher
from models.users import User
from fastapi.encoders import jsonable_encoder
from schemas.users import ShowAllUser, UserCreate, UserUpdate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        date_naissance=user.date_naissance,
        sexe=user.sexe,
        created_at=datetime.now()
        
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def update_user(
        db: Session,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

def all_user(db: Session)->List[ShowAllUser]:
    user = db.query(User).all()
    return user