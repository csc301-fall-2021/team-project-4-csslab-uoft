We want to run fastapi with `systemd` so it will be handled automatically. Here's a sample service file


Note I'm using hard coded paths from my local user account, you will want to change this

```[Unit]
Description=Gunicorn manager for Uvicorn serving maia_dash_api
After=network.target

[Service]
User=reidmcy
Group=www-data
WorkingDirectory=/home/reidmcy/team-project-4-csslab-uoft/dashboard_backend
ExecStart=/home/reidmcy/miniconda/bin/gunicorn --timeout 1000 --env GUNICORN_DEPLOY=PROD --log-file logs/activity.log --access-logfile logs/main_access.log --workers 6  --worker-class uvicorn.workers.UvicornWorker --bind unix:services/maia_dash_api.sock -m 007 main:app

[Install]
WantedBy=multi-user.target
```
