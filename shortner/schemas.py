import uuid
from pydantic import BaseModel
from fastapi import Form
from auth.schemas import UserOut
import datetime


class ShortenUrlCreate(BaseModel):
    original_url: str

    @classmethod
    def as_form(cls, url: str):
        return cls(original_url=url)

    class Config:
        from_attributes = True


class ShortenUrlOut(BaseModel):
    id: uuid.UUID
    code: str
    original_url: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    user: UserOut
