
from pydantic import BaseModel



class Msg(BaseModel):
    error: str
    message: str