import os

from fastapi import FastAPI

from dotenv import load_dotenv

from src.users.router import router as users_router
from src.receipts.router import router as receipts_router

load_dotenv(os.path.abspath('.env'))

app = FastAPI(
    docs_url='/docs',
    # Disable ReDoc Docs
    redoc_url=None,
    version=os.getenv('VERSION')
)

app.include_router(
    users_router,
    tags=['Users']
)
app.include_router(
    receipts_router,
    tags=['Receipts']
)
