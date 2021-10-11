import fastapi
import fastapi.responses

from .jwt_management import JWTBearer, signJWT
from .auth_schemas import JWT_Response, gen_user_name
from .auth_db import (
    get_user_info,
    register_user_db,
    log_user_login,
    default_username,
)

auth_router = fastapi.APIRouter(prefix="/auth",tags=['Auth'])

jwt_contr = JWTBearer()


@auth_router.get("/register", response_model=JWT_Response)
async def register_user(background_tasks: fastapi.BackgroundTasks):
    user_id = gen_user_name()
    background_tasks.add_task(register_user_db, user_id)
    return {
        "user_id": user_id,
        "jwt": signJWT(user_id),
        "provided_username": default_username,
        "lichess_username": None,
    }


@auth_router.post("/login_id")
async def login_id(
    background_tasks: fastapi.BackgroundTasks,
    user_id: str,
    screen_width: int,
    screen_height: int,
):
    user_dict = await get_user_info(user_id)
    if user_dict is None:
        raise fastapi.HTTPException(
            status_code=403,
            detail=f"Unreconized user ID: '{user_id}'.",
        )
    background_tasks.add_task(log_user_login, "user_id", screen_width, screen_height)
    return {
        "user_id": user_id,
        "provided_username": user_dict["provided_username"],
        "lichess_username": user_dict["lichess_username"],
        "jwt": signJWT(user_id),
    }


@auth_router.get("/add_get_user_info")
async def add_get_user_info(token: dict = fastapi.Depends(jwt_contr)):
    return await get_user_info(token["user_id"])
