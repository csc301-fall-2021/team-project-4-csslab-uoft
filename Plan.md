# 2021-10-10 Steps

Local:
- Basic FastAPI app - done
- Basic react app - done
- react talks to fastapi backend locally - done
- Install mongodb

Deploy
- deploy manually and have nginx refer to FastAPI
- deploy react app and have nginx refer to react.
- 


# Running backend
the `--bind` part will determine the port listened to.
```
gunicorn -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:7000 main:app
```
