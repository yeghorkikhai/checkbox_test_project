import os

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from dotenv import load_dotenv

from src.middlewares.database import DatabaseMiddleware

from src.database import Database, DATABASE_URL
from src.users.router import router as users_router
from src.receipts.router import router as receipts_router

from src.settings import Settings

load_dotenv(os.path.abspath('.env'))

app = FastAPI(
    # Swagger Docs
    docs_url='/docs',
    # Disable ReDoc Docs
    redoc_url=None,
    version=os.getenv('VERSION')
)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(
    users_router,
    tags=['Users']
)
app.include_router(
    receipts_router,
    tags=['Receipts']
)

database = Database(DATABASE_URL)
app.add_middleware(BaseHTTPMiddleware, dispatch=DatabaseMiddleware(database.sessionmaker))
