# app / routers / customer.py

from fastapi import APIRouter, Body
from app.database import customer, get_next_sequence
from datetime import datetime

router = APIRouter(prefix="/api/customer")

# 회원가입 => 127.0.0.1:8000/api/customer/join
@router.post("/join")
async def join_customer(
    email: str = Body(...),
    name: str = Body(...),
    password: str = Body(...),
    phone: str = Body(...)
):
    try:
        seq = await get_next_sequence("customer")
        await customer.insert_one(
            {
                "no": seq,
                "email": email,
                "name": name,
                "password": password,
                "phone": phone,
                "create_at": datetime.now(),
            }
        )
        return {"message": "회원 가입이 되었습니다."}
    except Exception as e:
        return {"message": str(e)}
