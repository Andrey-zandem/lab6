from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="REST API для заметок")


class NoteCreate(BaseModel):
    """Модель данных для создания заметки."""

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class Note(NoteCreate):
    """Модель заметки с идентификатором."""

    id: int


# Хранилище заметок в памяти программы.
notes: dict[int, Note] = {}

# Счётчик для автоматического назначения ID.
next_id: int = 1


@app.get("/notes")
def get_notes() -> list[Note]:
    """Получить список всех заметок."""
    return list(notes.values())


@app.get("/notes/{note_id}")
def get_note(note_id: int) -> Note:
    """Получить заметку по идентификатору."""
    note = notes.get(note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Заметка не найдена"
        )

    return note


@app.post("/notes", status_code=201)
def create_note(note_data: NoteCreate) -> Note:
    """Создать новую заметку."""
    global next_id

    note = Note(
        id=next_id,
        **note_data.model_dump()
    )

    notes[next_id] = note
    next_id += 1

    return note


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_data: NoteCreate) -> Note:
    """Полностью обновить существующую заметку."""
    if note_id not in notes:
        raise HTTPException(
            status_code=404,
            detail="Заметка не найдена"
        )

    note = Note(
        id=note_id,
        **note_data.model_dump()
    )

    notes[note_id] = note

    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int) -> dict[str, str]:
    """Удалить заметку."""
    if note_id not in notes:
        raise HTTPException(
            status_code=404,
            detail="Заметка не найдена"
        )

    del notes[note_id]

    return {"message": "Заметка успешно удалена"}