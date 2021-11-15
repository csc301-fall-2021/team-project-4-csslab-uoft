import time
import typing

import jwt #pyjwt

import fastapi
import fastapi.security

SECRET = "JWT_SECRET_TODO_MAKE_BETTER"

ALGO = "HS256"
jwt_duration = 120 #seconds


def signJWT(user_id: str) -> typing.Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + jwt_duration}
    token = jwt.encode(payload, SECRET, algorithm=ALGO)
    return {"access_token": token}


def decodeJWT(token: str) -> dict:
    if token.startswith("access_token: "):
        token = token.replace("access_token: ", "")
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=[ALGO])
    except jwt.DecodeError:
        return None
    if decoded_token["expires"] >= time.time():
        return decoded_token
    else:
        return None


async def register(user_id):
    return signJWT(user_id)


class JWTBearer(fastapi.security.HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: fastapi.Request):
        credentials: fastapi.security.HTTPAuthorizationCredentials = (
            await super().__call__(request)
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise fastapi.HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme.",
                )
            jwt_tkn = decodeJWT(credentials.credentials)
            if jwt_tkn:
                return jwt_tkn
            raise fastapi.HTTPException(
                status_code=403,
                detail="Invalid token or expired token.",
            )
        else:
            raise fastapi.HTTPException(
                status_code=403,
                detail="Invalid authorization code.",
            )
