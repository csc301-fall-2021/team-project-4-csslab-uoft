import random
import typing

import pydantic

import jwt #pyjwt

from .jwt_management import jwt_duration


def gen_user_name():
    return f"dash-guest-{random.randint(100000,1000000)}"


class JWT_Token(pydantic.BaseModel):
    access_token: str = jwt.encode(
        {
            "user_id": "example",
            "expires": 0,
        },
        "NOT THE REAL SECRET",
        algorithm="HS256",
    )


class JWT_Response(pydantic.BaseModel):
    user_id: str = gen_user_name()
    jwt: JWT_Token
    jwt_duration: int = jwt_duration
    provided_username: typing.Optional[str] = None
    lichess_username: typing.Optional[str] = None
