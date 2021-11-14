from datetime import datetime, timedelta
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token, create_refresh_token
from crud.login import get_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from schemas.tokens import ResponseToken, TokenData
from sqlalchemy.orm import Session


router = APIRouter()


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=ResponseToken)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    message = "L'utilisateur a été authentifié succés"
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        expire: str = payload.get("exp")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token error",
        )
    user = get_user(username,db)
    token_data = TokenData(email=username, expires=expire)
    user = get_user(username=username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )

    if datetime.utcnow().replace(tzinfo=None) > token_data.expires.replace(tzinfo=None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="expires token",
        )
    return user
