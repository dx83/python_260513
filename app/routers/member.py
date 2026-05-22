# app / routers / member.py

from fastapi import APIRouter, Body, Form, Depends
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer, JwtAuthorizationCredentials
from datetime import datetime, timedelta
from app.database import member
from passlib.context import CryptContext

router = APIRouter(prefix="/api/member", tags=["member"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 해쉬 함수
def hash_password(pw:str) -> str:
    return pwd_context.hash(pw)

#  암호 비교 함수
def verify_password(pw1:str, pw2:str) -> bool:
    return pwd_context.verify(pw1, pw2)

# access_token
access_token = JwtAccessBearer(
    secret_key="fd1iu3irej!@#%%61^!@4)#k",
    auto_error=True,
    access_expires_delta=timedelta(minutes=30)
)

# refresh_token (HMAC + SHA256)
refresh_token = JwtRefreshBearer(
    secret_key="3jdo1n5@f(lfo!fk98^nj#fd",
    auto_error=True,
    refresh_expires_delta=timedelta(days=1)
)


# 회원 탈퇴 => 127.0.0.1:8000/api/member/delete
# {"id": "a", "pw": "1234"}
@router.delete("/delete")
async def delete(
    credentials:JwtAuthorizationCredentials = Depends(access_token),
    pw:str = Body(embed=True)
):
    try:
        # 토큰에서 id정보만 추출하기
        id = credentials.subject["id"]

        ret = await member.find_one({'id':id})
        if not ret: # 토큰 탈취자 대비
            return {"result": -1, "message": "존재하지 않는 아이디입니다."}
        
        # 암호가 맞는지 확인
        if not verify_password(pw, ret["pw"]):
            return {"result": -2, "message": "비밀번호가 일치하지 않습니다."}
        
        # 삭제
        ret = await member.delete_one({"id": id})
        return {"result": 1, "deleted_id": str(ret.deleted_count)}
    except Exception as e:
        print(e)
        return {"result": -1, "message": str(e)}


# 정보 변경 => 127.0.0.1:8000/api/member/update
# {"id": "a", "pw": "1234", "name": "aa", "phone" : "010-1234-5678"}
@router.put("/update")
async def update(
    credentials:JwtAuthorizationCredentials = Depends(access_token),
    name:str = Body(...),
    phone:str = Body(...)
):
    try:
        # print(credentials) : 모르면 찍어보기
        # 토큰에서 id정보만 추출하기
        id = credentials.subject["id"]
        # 변경할 내용
        t1 = { "name": name, "phone": phone }

        ret = await member.update_one({"id":id}, {"$set":t1})
        return {"result": 1, "updated_id": str(ret.modified_count)}
    except Exception as e:
        print(e)
        return {"result": -1, "message": str(e)}


# 로그인 => 127.0.0.1:8000/api/member/login
# {"id": "a", "pw": "1234"}
@router.post("/login")
async def login(
    id:str = Body(...),
    pw:str = Body(...)
):
    try:
        doc = await member.find_one({"id":id})
        if not doc:
            return {"result":-1, "message": "존재하지 않는 아이디입니다."}
        
        if not verify_password(pw, doc["pw"]):
            return {"result":-2, "message": "비밀번호가 일치하지 않습니다."}
        
        # 토큰 발급
        acc_token = access_token.create_access_token({"id":id})
        ref_token = refresh_token.create_refresh_token({"id":id})

        return {"result": 1, "access_token": acc_token, "refresh_token": ref_token}

    except Exception as e:
        return {"result": -1, "message": str(e)}


# 회원가입 => 127.0.0.1:8000/api/member/join
# {"id": "a", "pw": "1234", "name": "aa", "phone": "010-1234-5678"}
@router.post("/join")
async def join(
    id:str = Body(...),
    pw:str = Body(...),
    name:str = Body(...),
    phone:str = Body(...),
):
    try:
        # 동일아이디 체크
        doc = await member.find_one({"id":id})
        if doc:
            return {"result": -1, "message": "이미 존재하는 아이디입니다."}
        
        t1 = {
            "id": id,
            "pw": hash_password(pw),
            "name": name,
            "phone": phone,
            "create_at": datetime.now()
        }

        ret = await member.insert_one(t1)

        return {"result":1, "message": "회원가입 되었습니다.", "inserted_id": str(ret.inserted_id)}
    except Exception as e:
        print(e)
        return {"result": -1, "message": str(e)}
