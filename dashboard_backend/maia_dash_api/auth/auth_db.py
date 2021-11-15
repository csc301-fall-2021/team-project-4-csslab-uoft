import datetime

from ..database import get_dash_db

default_username = "dash-guest"


async def get_user_info(user_id):
    client = await get_dash_db()
    return await client.users.find_one({"_id": user_id})


async def log_auth_event(client, event_dict):
    event_dict.update({"event_date": datetime.datetime.now()})
    await client.auth_events.insert_one(event_dict)

async def set_lichess_username(user_id, user_name):
    client = await get_dash_db()
    await client.users.update_one(
        {"_id": user_id},
        {"$set": {"lichess_username": user_name}},
    )
    return await client.users.find_one({"_id": user_id})

async def register_user_db(user_id):
    client = await get_db()
    current_dt = datetime.datetime.now()
    result = await client.users.insert_one(
        {
            "_id": user_id,
            "user_id": user_id,
            "provided_username": default_username,
            "lichess_username": None,
            "creation_date": current_dt,
        }
    )
    return result


async def log_user_login(user_id, how, screen_width=None, screen_height=None):
    client = await get_dash_db()
    await log_auth_event(
        client,
        {
            "user_id": user_id,
            "how": how,
            "screen_width": screen_width,
            "screen_height": screen_height,
        },
    )


async def log_player_data(user_dict):
    client = await get_dash_db()
    await client["user_data"].insert_one(user_dict)


async def set_lichess_username(user_id, username):
    client = await get_dash_db()
    update_result = client.users.update_one(
        {"_id": user_id},
        {"$set": {"lichess_username": username}},
    )
    await log_auth_event(
        client,
        {
            "user_id": user_id,
            "event_type": "set_username",
            "lichess_name": True,
            "username": username,
        },
    )
    await update_result
    return user_id
