from fastapi import APIRouter
from pydantic import BaseModel, Field
from dataclasses import asdict
from dependency_injector.wiring import inject, Provide
from datetime import datetime
from typing import Annotated
from fastapi import Depends, APIRouter
from common.auth import get_current_user, CurrentUser
from note.application.note_service import NoteService
from containers import Container

router = APIRouter(prefix="/notes")

class NoteResponse(BaseModel):
    id: str
    user_id:str
    title: str
    content: str
    memo_date:str
    tags: list[str]
    created_at: datetime
    updated_at: datetime

class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(
        default=None, min_length=1, max_length=32
    )    

class GetNoteResponse(BaseModel):
    total_count: int
    page: int
    notes: list[NoteResponse]

class UpdateNoteBody(BaseModel):
    title: str | None = Field(min_length=1, max_length=64, default=None)
    content: str | None = Field(min_length=1, default=None)
    memo_date: str | None = Field(min_length=8, max_length=8, default=None)
    tags: list[str] | None = Field(default=None)

@router.get("", response_model=GetNoteResponse)
@inject
def get_notes(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )
    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {
        "total_count": total_count,
        "page": page,
        "notes": res_notes,
    }

@router.post("", status_code=201, response_model=NoteResponse)
@inject
def create_note(
    body: CreateNoteBody,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.create_note(
        user_id=current_user.id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags if body.tags else [],
    )
    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response

@router.get("/{id}", response_model=NoteResponse)
@inject
def get_note(
    id: str,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.get_note(
        user_id=current_user.id,
        id=id,
        )
    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response

@router.put("/{id}", response_model=NoteResponse)
@inject
def update_note(
    id:str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateNoteBody,
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note=note_service.update_note(
        user_id=current_user.id,
        id=id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags,
    )
    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})
    return response

@router.delete("/{id}", status_code=204)
@inject
def delete_note(
    id: str,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note_service.delete_note(
        user_id=current_user.id,
        id=id,
    )

@router.get("/tags/{tag_name}/notes", response_model=GetNoteResponse)
@inject
def get_notes_by_tag(
    tag_name: str,
    page: int =1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes_by_tag(
        user_id=current_user.id,
        tag_name=tag_name,
        page=page,
        items_per_page=items_per_page,
    )
    
    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {
        "total_count": total_count,
        "page": page,
        "notes": res_notes,
    }