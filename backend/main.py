from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from constants import SERVER_URL as ENV_SERVER_URL, PORT as ENV_PORT, ENV as ENV_ENV
from apps.calculator.route import router as calculator_router

# Set SERVER_URL, PORT, and ENV with defaults if not present in environment
SERVER_URL = os.getenv("SERVER_URL", ENV_SERVER_URL or "127.0.0.1")  # Defaults to '127.0.0.1'
PORT = int(os.getenv("PORT", ENV_PORT or 8000))  # Defaults to port 8000 and casts to int
ENV = os.getenv("ENV", ENV_ENV or "prod")  # Defaults to 'prod'

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# Adding the CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def health():
    return {'message': 'Server is running'}

# Include the router for your calculator app
app.include_router(calculator_router, prefix='/calculate', tags=['calculate'])

if __name__ == "__main__":
    # The reload option should be a boolean, based on the ENV value
    reload_option = (ENV == 'dev')  # Only reload in development
    uvicorn.run("main:app", host=SERVER_URL, port=PORT, reload=reload_option)
