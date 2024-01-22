from typing import List

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.events import Event

router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

# 새로운 레코드 추가
@router.post("/new")
async def create_event(body: Event) -> dict: # 형식을 body:Event로 지정
    # save 사용은 동일하나, body라는 변수를 넣어 줌. 
    document = await event_database.save(body)
    return {
        "message": "Event created successfully"
        ,"datas": document
    }

# id 기준 한 row 확인
@router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# id에 따른 row 삭제
@router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    event = await event_database.delete(id)

    return {
        "message": "Event deleted successfully."
        ,"datas": event
    }

# put == update
from fastapi import Request
@router.put("/{id}", response_model=Event)
async def update_event_withjson(id: PydanticObjectId, request:Request) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    body = await request.json()
    updated_event = await event_database.update_withjson(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

# # list로 전체 내용 가져오기
# @router.get("/", response_model=List[Event])
# async def retrieve_all_events() -> List[Event]:
#     events = await event_database.get_all()
#     return events

# # response_model=List[Event] 삭제하고 return 형식 변경?!
@router.get("/")
async def retrieve_all_events() -> dict:
    events = await event_database.get_all()
    return {"total_count":len(events),
            'datas':events}