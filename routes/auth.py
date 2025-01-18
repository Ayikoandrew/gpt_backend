from typing import Annotated
import uuid
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from db.database import get_db
from model.users import Login, Users

router = APIRouter()
sessionDep = Annotated[Session, Depends(get_db)]


@router.post("/signup")
def signup(user: Users, session: sessionDep):
    statement = select(Users).where(Users.email == user.email)
    result = session.exec(statement).first()

    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    new_user = Users(
        id=str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(user: Login, session: sessionDep):
    statement = select(Users).where(Users.email == user.email)
    result = session.exec(statement).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential"
        )

    isPassword = bcrypt.checkpw(user.password, result.password)

    if not isPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credential"
        )

    return result
