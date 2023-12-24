from typing import Annotated

import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class TelegramUser(BaseModel):
    telegram_id: int
    name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/telegram-users")
async def create_telegram_user(tg_user: TelegramUser, db: db_dependency):
    db_tg_user = models.TelegramUser(telegram_id=tg_user.telegram_id, name=tg_user.name)
    db.add(db_tg_user)
    db.commit()
    db.refresh(db_tg_user)
