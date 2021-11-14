from pydantic import BaseModel
from pydantic import EmailStr
from datetime import date, datetime
from typing import Optional


class UserBase(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    sexe: Optional[str]

# properties required during user creation
class UserCreate(UserBase):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    date_naissance: date
    sexe: str

#properties optional durring user update
class UserUpdate(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    sexe: Optional[str]
    date_naissance:Optional[date]


class ShowOneUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    date_naissance:date
    sexe:str
    created_at:datetime

    class Config:  # to convert non dict obj to json
        orm_mode = True


class ShowAllUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    sexe:str

    class Config:  # to convert non dict obj to json
        orm_mode = True
