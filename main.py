from fastapi import FastAPI
from config import engine, metadata
import config
import router

config.Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(router.router,prefix="/customer",tags=["customer"])