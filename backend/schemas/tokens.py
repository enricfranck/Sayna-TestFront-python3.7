from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ResponseToken(BaseModel):
    error: bool
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    created_at:datetime

class TokenData(BaseModel):
    email:Optional[str]
    expires:Optional[datetime]
