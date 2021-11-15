import hashlib
import urllib.parse
import datetime

import requests

import fastapi
import fastapi.responses
import starlette.requests

from authlib.oauth2.rfc7636 import create_s256_code_challenge

from .auth_router import auth_router
from .jwt_management import decodeJWT, signJWT, jwt_duration
from .auth_db import set_lichess_username, log_player_data

LICHESS_CLIENT_ID = "RANDOM_ID_TODO_MAKE_BETTER"
LICHESS_CODE_CHALLENGE = "RANDOM_CHALLENGE_TODO_MAKE_BETTER"


def make_code_challenge(user_id):
    return (
        hashlib.md5(f"{LICHESS_CODE_CHALLENGE}-{user_id}".encode("utf8")).hexdigest()
        + hashlib.md5(f"{user_id}-{LICHESS_CODE_CHALLENGE}".encode("utf8")).hexdigest()
    )


@auth_router.get("/lichess_login/{jwt_token}")
async def login_via_lichess(
    jwt_token: str,
    request: starlette.requests.Request,
    redirect_path: str = "turing",
):
    jwt_token_decode = decodeJWT(jwt_token)
    if jwt_token_decode is None:
        raise fastapi.HTTPException(
            status_code=403,
            detail="Invalid token or expired token.",
        )
    if redirect_path.startswith("/"):
        redirect_path = redirect_path[1:]
    query_dict = {
        "response_type": "code",
        "client_id": LICHESS_CLIENT_ID,
        "redirect_uri": request.url_for("auth_via_lichess"),
        "state": f"{jwt_token}+{redirect_path}",
        "code_challenge_method": "S256",
        "code_challenge": create_s256_code_challenge(
            make_code_challenge(jwt_token_decode["user_id"])
        ),
    }

    print(query_dict)
    query_url = f"https://lichess.org/oauth?{urllib.parse.urlencode(query_dict)}"
    response = fastapi.responses.RedirectResponse(query_url)
    response.set_cookie(
        key="jwt_token",
        value=jwt_token,
        expires=jwt_duration + 1,
    )
    return response


@auth_router.get(f"/lichess_authorize")
async def auth_via_lichess(
    request: starlette.requests.Request,
    background_tasks: fastapi.BackgroundTasks,
    code: str = None,
    state: str = None,
):
    jwt_token, redirect_path = state.split("+")[:2]
    jwt_token_decode = decodeJWT(jwt_token)
    if jwt_token_decode is None:
        raise fastapi.HTTPException(
            status_code=403,
            detail="Invalid token or expired token.",
        )
    dat = {
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": make_code_challenge(jwt_token_decode["user_id"]),
        "redirect_uri": request.url_for("auth_via_lichess"),
        "client_id": LICHESS_CLIENT_ID,
    }
    req = requests.post("https://lichess.org/api/token", data=dat)
    li_dict = req.json()
    header = {"Authorization": f"Bearer {li_dict['access_token']}"}
    user_req = requests.get("https://lichess.org/api/account", headers=header)
    user_dict = user_req.json()
    await set_lichess_username(jwt_token_decode["user_id"], user_dict["id"])
    user_dict["user_id"] = jwt_token_decode["user_id"]
    user_dict["server_timestamp"] = datetime.datetime.now()
    background_tasks.add_task(log_player_data, user_dict)
    return fastapi.responses.RedirectResponse(
        f"https://survey.maiachess.com/{redirect_path}"
    )
