# 2021-10-10 Steps

Local:
- Basic FastAPI app - done
- Basic react app - done
- react talks to fastapi backend locally - done
- Install mongodb - done
- Connect FastAPI to mongodb - done

Deploy
- deploy manually and have nginx serve FastAPI + react
- create github actions to deploy
- 

# Local work

## Running mongodb container 
Install Docker and run from the top directory of the project:
```
docker-compose up
```
To test that it works, go to `http://localhost:27017` in your browser,
You should see a message: `It looks like you are trying to access MongoDB over HTTP on the native driver port.`.

If you do not see this message, something is wrong starting mongodb container.

## Running backend
You can either run the server from the command line using this command from the `backend` directory:
```
uvicorn main:app --host 0.0.0.0 --port 7000
```

Or alternatively, you can run the `main.py` using your IDE.
If you wish to change the port the app is running on, you can change this line in `main.py`
```
uvicorn.run(app, host="0.0.0.0", port=8000) # << Change port
```

If you want your FastAPI to point to a different mongo database, you 
can set an environment variable `MONGODB_URL` to where you have your mongodb instance.

To check that your backend works, go to `http://localhost:7000/docs` - you should see the 
FastAPI openapi doc and you can test the basic API (students CRUD).

## Running frontend
From the `frontend` directory, run 
```
npm start
```
This will start the react app locally. 
Notice it proxies requests to the backend on port 7000 - If you wish to change that, 
update under `packages.json` the line:
```
"proxy": "http://127.0.0.1:7000",
```



