import fastapi
import uvicorn
import starlette.requests
import starlette.middleware.sessions
import starlette.middleware.gzip

import fastapi.staticfiles
import fastapi.middleware.cors

import maia_dash_api

#Test run with
#uvicorn main:app --reload --port 32580 --host 0.0.0.0
#Docs at http://dashboard.maiachess.com:32580/api/docs

app = fastapi.FastAPI(
    version=maia_dash_api.__version__,
    docs_url="/api/docs",
    openapi_url="/api/v1/openapi.json",
)

#Allow NGINX to proxy
app.add_middleware(
    uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware,
    trusted_hosts="*",
)

#Disable CORS
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Connect to Mongo on startup
app.add_event_handler("startup", maia_dash_api.db_connect)
app.add_event_handler("shutdown", maia_dash_api.db_disconnect)

#Have different components be handled separately
app.include_router(maia_dash_api.auth_router)

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/")
async def root():
    return fastapi.responses.PlainTextResponse("WORKING")
