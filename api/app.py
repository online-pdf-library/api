from fastapi import FastAPI

from api import api, middlewares

app = FastAPI()


api.include_routers(app)
middlewares.add_middlewares(app)
