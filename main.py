# main.py
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from app import server as dash_server

app = FastAPI()

# Mount the Dash application as a sub-application
app.mount("/", WSGIMiddleware(dash_server))