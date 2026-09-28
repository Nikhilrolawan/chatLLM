from models import model
from schemas import schema
from fastapi import APIRouter, Depends, Sess
from db.engine import get_db
from sqlalchemy import select
import bcrypt
import jwt
import os


JWT_SECRET = os.getenv("JWT_SECRET")
router = APIRouter(prefix="/auth", tags =["auth"])

@router.post("/signup")
async def signup(body: schema.CreateUser, db = Depends(get_db)):
    name, email, password = body.name, body.email, body.password
    user = model.User
    query = select(user).where(user.email == email)
    res = await db.execute(query)
    exist = res.scalar_one_or_none()
    if exist:
        return {"msg":"User already exist"}
    
    hash_password = bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=bcrypt.gensalt(),
    )

    user = model.User(
        name = name,
        email = email,
        password = hash_password,
    )
    db.add(user)
    await db.commit()

    return {
        "msg": "User created successfully"
    }

@router.post("/login")
async def login(body: schema.CreateUser, db = Depends(get_db)):
    _, email, password = body.name, body.email, body.password
    user = model.User
    query = select(user.email, user.hashed_pass).where(user.email == email)
    res = await db.execute(query)
    exist = res.one_or_none()
    
    if not exist:
        return {"msg":"User doesn't exist create a new account"}
    
    db_mail, db_pass = exist

    password_valid = bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=db_pass.encode("utf-8"),
    )
    if not password_valid:
        return {
            "msg": "Invalid Credtials"
        }
    token = jwt.encode(
        payload={
            "email": db_mail
        },
        key = JWT_SECRET,
        algorithm = "HS256"
    )
    return {
        "token": token
    }