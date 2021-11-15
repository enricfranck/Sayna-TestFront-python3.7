from apis.version1.route_login import get_current_user_from_token
from fastapi import HTTPException
from core.config import settings
from schemas.tokens import ResponseToken
from crud.users import all_user, create_new_user, get_user_by_email, update_user
from core.security import create_access_token, create_refresh_token
from db.session import get_db
from schemas.msg import Msg
from schemas.users import ShowAllUser, ShowOneUser, UserUpdate
from typing import List, Union
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from datetime import datetime, timedelta
from schemas.users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users", response_model=List[ShowAllUser])
def get_all_user_(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_token) , 
    ):
    users = all_user(db=db)
    return users


@router.post("/register", response_model=ResponseToken)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(email=user_in.email, db=db)
    if user :
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email",
        )

    user = create_new_user(user=user_in, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="votre email n'est pas correct",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    message = "L'utilisateur a bien été créé avec succés"
    date_now = datetime.now()
    refresh_token = create_refresh_token(user.email)
    return {
        "error":False,
        "message": message,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "created_at": date_now,
        "token_type": "bearer"
        
    }

@router.get("/user", response_model=ShowOneUser)
def get_user_(
    current_user = Depends(get_current_user_from_token) , 
    db: Session = Depends(get_db)):
    return current_user

@router.put("/user", response_model=Union[Msg, ShowOneUser])
def update_user_(
    user_in: UserUpdate,
    current_user = Depends(get_current_user_from_token) , 
    db: Session = Depends(get_db)):
    if current_user.email is not None:
        user_oj=get_user_by_email(current_user.email, db)
        user = update_user(db=db, db_obj=user_oj,obj_in=user_in,) 
        if user:
            return{
                "error":False,
                "message":"L'utilisateur a été modifié succés"
            }
    return current_user

