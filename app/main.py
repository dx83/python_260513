# 파일명 : app / main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import board, member, item, customer, fish, predict
import joblib

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("./pkl/20260519_lasso.joblib")
    app.state.image_model = joblib.load("./pkl/20260527_image_model.joblib")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(board.router)
app.include_router(member.router)
app.include_router(item.router)
app.include_router(fish.router)
app.include_router(predict.router)

app.include_router(customer.router) # 개인실습

'''
최초 확인
from fastapi import FastAPI
app = FastAPI()
# 127.0.0.1:8000 -> Hello World
@app.get("/")
def read_root():
    return {"Hello":"World"}
'''
