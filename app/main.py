# 파일명 : app / main.py

from fastapi import FastAPI
from app.routers import board, member, item, customer

app = FastAPI()

app.include_router(board.router)
app.include_router(member.router)
app.include_router(item.router)

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
