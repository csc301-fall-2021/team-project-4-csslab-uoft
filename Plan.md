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

# Running mongodb container 
```
docker-compose up
```

# Running backend

## Environment variables
```
export MONGODB_URL="mongodb://root:example@127.0.0.1:27017/students?retryWrites=true&w=majority"
```

the `--bind` part will determine the port listened to.
```
gunicorn -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:7000 main:app
```
Alternative (better) command:
```
uvicorn main:app --host 0.0.0.0 --port 7000
```
