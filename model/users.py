from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password: bytes


class Login(SQLModel):
    email: EmailStr
    password: bytes
