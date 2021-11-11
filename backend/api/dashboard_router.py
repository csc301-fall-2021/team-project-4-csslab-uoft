import fastapi

from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId, json_util
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException, status
from .utils import PyObjectId
from . import db_client
from .models import EventModel, UserModel
import json
import lichess.api
import lichess.format

dashboard_router = fastapi.APIRouter(prefix="/api/dashboard", tags=['dashboard'])


class DBUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user: str = Field(...)
    num_games: int = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
            }
        }


@dashboard_router.post("/events", response_description="Log frontend event")
async def log_fe_event(event: EventModel = Body(...)):
    event_json = jsonable_encoder(event)
    client = db_client.get_dashboard_db()
    new_event = await client["events"].insert_one(event_json)
    created_event = await client["events"].find_one({"_id": new_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_event)


@dashboard_router.get("/lichess_users/{username}", response_description="Get user profile from Lichess",
                      response_model=UserModel)
async def get_user_profile_from_lichess(username: str):
    try:
        lichess_info = lichess.api.user(username)
    except lichess.api.ApiError as err:
        return JSONResponse(status_code=status.HTTP_200_OK, content=None)

    ret = {"lichess_id": username, "lichess_info": lichess_info}
    return JSONResponse(status_code=status.HTTP_200_OK, content=ret)


@dashboard_router.get("/users/{username}", response_description="Check if username is in Maia DB",
                      response_model=DBUserModel)
async def find_username_in_maia_db(username: str):
    client = db_client.get_dashboard_db()
    table = client["user_data"]
    exists = await table.find_one({"user": username})
    if exists is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json_util.dumps(exists)))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=None)


@dashboard_router.post("/users/{username}", response_description="Add username to Maia DB", response_model=DBUserModel)
async def add_username_to_maia_db(username: str):
    new_user_data = {
        "user": username,
        "num_games": 0
    }
    client = db_client.get_dashboard_db()
    table = client["user_data"]

    exists = await table.find_one({"user": username})
    if exists is not None:
        return JSONResponse(status_code=status.HTTP_306_RESERVED, content={"reserved": username + " already exists"})

    new_user = await table.insert_one(new_user_data)
    created_user = await table.find_one({"_id": new_user.inserted_id})

    ret = json.loads(json_util.dumps(created_user))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=ret)


@dashboard_router.post("/login/{username}/{oauthtoken}", response_description="Login with Lichess")
async def login(username: str, oauthtoken: str):
    try:
        games = lichess.api.user_games(username=username, max=10, auth=oauthtoken, format=lichess.format.PGN)
        pgns = list(games)
    except lichess.api.ApiHttpError as err:
        return JSONResponse(status_code=status.HTTP_206_PARTIAL_CONTENT, content={"status": "Authentication failed"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"status": "Authentication succeeded. Pulled 10 sample games", "games": pgns})


@dashboard_router.get("/logout/{username}", response_description="Logout")
async def logout(username: str):
    ret = {
        "status": "stubbed logout for " + username + " no action to take here as of yet"
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=ret)
