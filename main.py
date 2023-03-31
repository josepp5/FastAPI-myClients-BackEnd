from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine, Customer
from dotenv import load_dotenv
import config
import router
import jwt_auth_users

config.Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv()

app.include_router(router.router,prefix="/customer",tags=["customer crud"])
app.include_router(jwt_auth_users.app, tags=["login"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    )
