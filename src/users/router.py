from fastapi import APIRouter

router = APIRouter()


@router.post('/users')
async def register_user(name: str, login: str, password: str):
    ...