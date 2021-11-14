from datetime import datetime
from datetime import timedelta
from typing import Optional
from schemas.msg import Msg
from pydantic.networks import EmailStr
from fastapi import Depends
from core.config import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(email: EmailStr):
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub":str(email)}, expires_delta=expires)


def is_valid_data(error: str) -> Msg:
    if error == "field required":
        return {
            "error":True,
            "message":"L'une ou plusieures des donnéés obligatoire sont manquantes"
        }
    else:
        return {
            "error":True,
            "message":"L'un des donnéés obligatoire ne sont pas conforme"
        }

def is_valid_token(error: str) -> Msg:
    if error == "token error":
        return{
                "error":True,
                "message":"Le token envoyez n'est pas conforme"
            }
    elif error == "invalid token":
        return{
            "error":True,
            "message":"Le token envoyez n'existe pas"
        }
    elif error == "expires token":
         return{
            "error":True,
            "message":"Votre token n'est plus valide, veuillez le réinitialiser"
        }
    elif error == "invalid email":
        return{
            "error":True,
            "message":"Votre email ou password est erooné"
        }
    else:
        return{
            "error":error
        }