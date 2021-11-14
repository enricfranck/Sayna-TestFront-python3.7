from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from db.session import SessionLocal
from db.utils import check_db_connected
from fastapi import FastAPI, status, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Any
from core.security import is_valid_data,is_valid_token


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, responses={
        422: {
            "description":"validation Error",
            "model":Any
        }
    })

def include_router(app):
    # app.add_exception_handler(ValidationExceptionHandler,validation_exception_handler)
    app.include_router(api_router, responses={
        422: {
            "description":"validation Error",
            "model":Any
        }
    })


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    db = SessionLocal()
    include_router(app)
    create_tables()
    return app

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exec:RequestValidationError ):
    error = exec.errors()[0]['msg']
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = jsonable_encoder(is_valid_data(error))
    )
@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exec:HTTPException ):
    return JSONResponse(
        status_code = status.HTTP_401_UNAUTHORIZED,
        content = jsonable_encoder(is_valid_token(exec.detail))
    )

app = start_application()



@app.on_event("startup")
async def app_startup():
    await check_db_connected()
