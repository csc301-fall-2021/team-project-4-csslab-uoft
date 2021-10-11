import motor.motor_asyncio


class DataBase:
    client: motor.motor_asyncio.AsyncIOMotorClient = None


db = DataBase()


async def get_dash_db():
    return db.client["test_dashboard"]

async def get_analysis_db():
    return db.client["test_analysis"]

async def db_connect():
    db.client = motor.motor_asyncio.AsyncIOMotorClient()


async def db_disconnect():
    db.client.close()


async def write_one_dash(table, data):
    client = await get_dash_db()
    await client[table].insert_one(data)
