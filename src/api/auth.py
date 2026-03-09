from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    EmailAlreadyExistsHTTPException,
    UserAlreadyExistsException,
    EmailNotFoundException,
    EmailNotFoundHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise EmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login", summary="Аутентификация")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotFoundException:
        raise EmailNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получение пользователя")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none(user_id)


@router.post("/logout", summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
