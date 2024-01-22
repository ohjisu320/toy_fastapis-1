from typing import List

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["users"]
)
users_database = Database(User)

# 새로운 레코드 추가
# http://127.0.0.1:8000/users_api/
# {    "name": "Ohjisu",
#     "email": "ohjisu320@gmail.com",
#     "pswd": "12345678",
#     "manager": "on",
#     "sellist1" : "Option1",
#     "text" : "안녕하세요"
# }
@router.post("/")
async def create_event(body: User) -> dict: # 형식을 body:Event로 지정
    # save 사용은 동일하나, body라는 변수를 넣어 줌. 
    document = await users_database.save(body)
    return {
        "message": "Users created successfully"
        ,"datas": document
    }


# id 기준 한 row 확인
# http://127.0.0.1:8000/users_api/{id}/{pswd}
# http://127.0.0.1:8000/users_api/65ae11d482bbdcb75e210406/12345678
@router.get("/{id}/{pswd}", response_model=User)
async def retrieve_event(id: PydanticObjectId, pswd) -> User:
    conditions = { '_id':id,
                  'pswd':pswd}
    user = await users_database.getsbyconditions(conditions)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    return user[0]

# id에 따른 row 삭제
# http://127.0.0.1:8000/users_api/{id}
@router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    user = await users_database.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = await users_database.delete(id)

    return {
        "message": "User deleted successfully."
        ,"datas": user
    }

# put == update
# http://127.0.0.1:8000/users_api/{id}
from fastapi import Request
@router.put("/{id}", response_model=User)
async def update_event_withjson(id: PydanticObjectId, request:Request) -> User:
    user = await users_database.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    body = await request.json()
    updated_event = await users_database.update_withjson(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    return updated_event

