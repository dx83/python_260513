# app/routers/item.py

from fastapi import APIRouter, Form, File, UploadFile, Body
from app.database import item, get_next_sequence
from datetime import datetime

from fastapi.responses import StreamingResponse, FileResponse
from io import BytesIO
from pathlib import Path
import uuid
import os

BASE_DIR = Path(__file__).resolve().parent.parent
filePath = BASE_DIR / "uploads"
print(filePath)

router = APIRouter(prefix="/api/item", tags=["item"])


# 물품목록 => 127.0.0.1:8000/api/item/list?page=1&limit=10
@router.get("/list")
async def get_item_list(page: int = 1, limit: int = 10):
    try:
        query = {}  # 조건
        projection = {
            "_id": 0,
            "filename": 0,
            "filedata": 0,
            "filetype": 0,
            "filesize": 0,
        }  # 제거할 컬럼
        skip = (page - 1) * limit  # 건너뛸 갯수

        total = await item.count_documents(query)  # 전체 갯수
        t1 = await item.find(query, projection).skip(skip).limit(limit).to_list(length=limit)

        # 반복문을 사용해서 새로운 imgurl 생성
        for doc in t1:
            doc["imgurl"] = f"/api/item/image?no={doc['no']}"

        return {"list": t1, "total": total}
    except Exception as e:
        return {"message": str(e)}


# 이미지표시 => 127.0.0.1:8000/api/item/image1?no=10004
@router.get("/image1")
async def get_image1(no: int):
    try:
        query = {"no": no}
        projection = {"filename": 1, "filetype": 1}
        t1 = await item.find_one(query, projection)
        print(no)
        if t1:
            return FileResponse(path=t1["filename"], media_type=t1["filetype"])
        else:
            return {"message": "이미지를 찾을 수 없습니다."}
    except Exception as e:
        return {"message": str(e)}


# 이미지등록 => 127.0.0.1:8000/api/item/insert1
# post방식으로 name, description, price, img
@router.post("/insert1")
async def insert_item1(
    title: str = Form(...),
    descrition: str = Form(...),
    price: int = Form(...),
    file: UploadFile = File(...),
):
    try:
        # 확장자
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"

        # 파일저장 위치
        save_path = f"{filePath}/{filename}"

        # 바이트스트림으로 읽어서 저장
        with open(save_path, "wb") as f:
            f.write(await file.read())

        t1 = {
            "no": await get_next_sequence("item"),
            "title": title,
            "description": descrition,
            "price": price,
            "filename": save_path,
            "filetype": file.content_type,
            "filesize": file.size,
            "create_at": datetime.now(),
        }
        ret = await item.insert_one(t1)
        return {"message": "success", "inserted_id": str(ret.inserted_id)}
    except Exception as e:
        return {"message": str(e)}


# 이미지표시 old => 127.0.0.1:8000/api/item/image?no=1
@router.get("/image")
async def get_image(no: int):
    try:
        query = {"no": no}
        projection = {"_id": 0}
        t1 = await item.find_one(query, projection)
        if t1:
            return StreamingResponse(BytesIO(t1["filedata"]), media_type=t1["filetype"])
        else:
            return {"message": "이미지를 찾을 수 없습니다."}
    except Exception as e:
        return {"message": str(e)}


# 이미지등록 old => 127.0.0.1:8000/api/item/insert
# post방식으로 name, description, price, img
@router.post("/insert")
async def insert_item(
    title: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    file: UploadFile = File(...),
):
    try:
        t1 = {
            "no": await get_next_sequence("item"),
            "title": title,
            "description": description,
            "price": price,
            "filename": file.filename,
            "filedata": await file.read(),
            "filetype": file.content_type,
            "filesize": file.size,
            "create_at": datetime.now(),
        }
        ret = await item.insert_one(t1)
        return {"message": "success", "inserted_id": str(ret.inserted_id)}
    except Exception as e:
        return {"message": str(e)}
