from note.domain.note import Note
from note.domain.repository.note_repo import INoteRepository
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from database import SessionLocal
from note.domain.repository.note_repo import INoteRepository
from note.domain.note import Note as NoteV0
from note.infra.db_models.note import Note, Tag
from utils.db_utils import row_to_dict

class NoteRepository(INoteRepository):
    def get_notes (
            self,
            user_id: str,
            page: int,
            items_per_page: int
    ) -> tuple[int,list[NoteV0]]:
        with SessionLocal() as db:
            query = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id)
            )

            total_count = query.count()
            notes = (
                query.offset((page - 1) * items_per_page)
                             .limit(items_per_page)
                             .all()
            )
            
        notes_vos = [NoteV0(**row_to_dict(note)) for note in notes]
                     
        return total_count, notes_vos    

    def find_by_id(self, user_id: str, id: str) -> NoteV0:
        with SessionLocal() as db:
            note = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(
                Note.user_id == user_id, Note.id == id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)
            return NoteV0(**row_to_dict(note)) 
        raise NotImplementedError
    
    def find_by_id(self, user_id: str, id: str) -> Note:
        raise NotImplementedError
    
    def save(self, user_id: str, note_vo: NoteV0):
     with SessionLocal() as db:
        tags: list[Tag] = []
        for tag in note_vo.tags:
            existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
            if existing_tag:
                tags.append(existing_tag)
            else:
                tags.append(
                    Tag(
                        id=tag.id,
                        name=tag.name,
                        user_id=user_id,
                        title=note_vo.title,
                        content=note_vo.content,
                        memo_date=note_vo.memo_date,
                        tags=tags,
                        created_at=note_vo.created_at,
                        updated_at=note_vo.updated_at
                    )
                )
            
            new_note = Note(
                id=note_vo.id,
                user_id=user_id,
                title=note_vo.title,
                content=note_vo.content,
                memo_date=note_vo.memo_date,
                tags=tags,
                created_at=note_vo.created_at,
                updated_at=note_vo.updated_at
            )

            db.add(new_note)
            db.commit()
        raise NotImplementedError
    
    def update(self, user_id: str, note_vo: NoteV0) -> NoteV0:
        with SessionLocal() as db:
            self.delede_tags(user_id, note_vo.id)

            note = (
                db.query(Note)
                .filter(Note.user_id == user_id, Note.id == note_vo.id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)

            note.title = note_vo.title
            note.content = note_vo.content
            note.memo_date = note_vo.memo_date

            tag: list[Tag] = []
            for tag in note_vo.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tag.append(existing_tag)
                else:
                    tag.append(
                        Tag(
                            id=tag.id,
                            name=tag.name,
                            created_at=note_vo.created_at,
                            updated_at=note_vo.updated_at,
                        )
                    )

            note.tags = tag

            db.add(note)
            db.commit()

            return NoteV0(**row_to_dict(note))
        raise NotImplementedError
    
    def delete(self, user_id: str, id: str):
        with SessionLocal() as db:
            self.delete_tags(user_id, id)

            note = db.query(Note).filter(
                Note.user_id == user_id, Note.id == id
            ).first()
            if not note:
                raise HTTPException(status_code=422)

            db.delete(note)
            db.commit()
        raise NotImplementedError
    
    def delete_tags(self, user_id: str, note_id: str):
        with SessionLocal() as db:
            note=db.query(Note).filter(
                Note.user_id == user_id, Note.id == id
                ).first()
            if not note:
                raise HTTPException(status_code=422)

            note.tags = []
            db.add(note)
            db.commit()

            unusd_tags=db.query(Tag).filter(~Tag.mptes/any()).all()
            for tag in unusd_tags:
                db.delete(tag)

            db.commit()    
        raise NotImplementedError
    
    def get_notes_by_tag_name(
            self,
            user_id: str,
            tag_name: str,
            page: int,
            items_per_page: int
    ) -> tuple[int, list[NoteV0]]:
        with SessionLocal() as db:
            tag = db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                return 0, []
            
            query = (
                db.query(Note)
                # .options(joinedload(Note.tags))
                .filter(
                    Note.user_id == user_id,
                    Note.tags.any(id=tag.id))
            )

            total_count = query.count()
            notes = (
                query.offset((page - 1) * items_per_page)
                .limit(items_per_page)
                .all()
            )

            notes_vos = [NoteV0(**row_to_dict(note)) for note in notes]
            return total_count, notes_vos
            
        raise NotImplementedError