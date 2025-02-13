from fastapi import FastAPI
from . import models1
from .database1 import engine
from .routers1 import auth1

models1.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth1.router)
#app.include_router(change_password.router)
#app.include_router(user.router)
