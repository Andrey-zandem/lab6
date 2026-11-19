from typing_extensions import TypedDict

from fastapi import FastAPI


class User(TypedDict):
    id: int
    name: str
    age: int


USERS: list[User] = [
    {
        "id": 1,
        "name": "Иван",
        "age": 20
    },
    {
        "id": 2,
        "name": "Сергей",
        "age": 21
    }
]

app: FastAPI = FastAPI()


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Привет FastAPI!"}


@app.get("/users")
def get_users() -> list[User]:
    return USERS
