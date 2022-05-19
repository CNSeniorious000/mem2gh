from fastapi import FastAPI
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"))


class Record(BaseModel):
    class_: str
    data: bytes


@app.post("/upload")
def add_record(record: Record):
    print(record)
