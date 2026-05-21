# app / routers / board.py

from fastapi import APIRouter, Body
from app.database import board, get_next_sequence
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/board", tags=["board"])

# 게시글 상세 => 127.0.0.1:8000/api/board/detail?no=1
@router.get("/detail")
async def detail_board(no:int):
    try:
        query = { "no":no }
        projection = { "_id":0 }
        return await board.find_one(query, projection)
    except Exception as e:
        return { "message": str(e) }

# 게시글 삭제 => 127.0.0.1:8000/api/board/delete
@router.delete("/delete")
async def delete_board(id: str = Body(embed=True)):
    try:
        # 조건
        query = {"_id": ObjectId(id)}
        # 삭제
        ret = await board.delete_one(query)
        print(ret)
        if ret.deleted_count == 1:
            return {"message": "글이 삭제되었습니다."}

        return {"message": "삭제할 글이 없습니다."}

    except Exception as e:
        return {"message": str(e)}


# 게시글 변경 => 127.0.0.1:8000/api/board/update
@router.put("update")
async def update_board(
    title: str = Body(...),
    content: str = Body(...),
    author: str = Body(...),
    id: str = Body(...),
):
    try:
        # 조건
        query = {"_id": ObjectId(id)}
        # 변경내용
        update = {"$set": {"title": title, "content": content, "author": author}}
        # 변경후 결과값 ret로 반환
        ret = await board.update_one(query, update)
        print(ret)
        if ret.modified_count == 1:
            return {"message": "글이 수정되었습니다."}

        return {"message": "수정할 글이 없습니다."}
    except Exception as e:
        return {"message": str(e)}


# 페이지네이션 => 127.0.0.1:8000/api/board/listpage?page=1&limit=5
@router.get("/listpage")
async def list_page(page: int = 1, limit: int = 5):
    try:
        query = {}
        projection = {"_id": 0}
        skip = (page - 1) * limit
        sort = {"_id": -1}
        return (
            await board.find(query, projection)
            .sort(sort)
            .skip(skip)
            .limit(limit)
            .to_list(length=100)
        )
    except Exception as e:
        return {"message": str(e)}


# 전체 글 보기 => 127.0.0.1:8000/api/board/list
@router.get("/list")
async def list_board():
    try:
        query = {}
        projection = {"_id": 0}
        return await board.find(query, projection).to_list(length=100)
    except Exception as e:
        return {"message": str(e)}


# 글쓰기 => 127.0.0.1:8000/api/board/write
@router.post("/write")
async def write_board(
    title: str = Body(...), content: str = Body(...), author: str = Body(...)
):
    try:
        seq = await get_next_sequence("board")
        await board.insert_one(
            {
                "no": seq,
                "title": title,
                "content": content,
                "author": author,
                "create_at": datetime.now(),
            }
        )
        return {"message": "글이 작성되었습니다."}
    except Exception as e:
        return {"message": str(e)}
