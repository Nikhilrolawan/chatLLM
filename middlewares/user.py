import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException, Depends
from sqlalchemy import select
from models import model
from db.engine import get_db
import jwt

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

async def get_current_user(authorization: str = Header(), db = Depends(get_db)):
    credential_exception = HTTPException(status_code=401, detail="Could not validate credentials")

    parts = authorization.split(" ")
    if len(parts) != 2: raise HTTPException(status_code=401, detail="invalid authorization header format")
    scheme, token = parts
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme"
        )
    try:
        payload = jwt.decode(
            jwt = token,
            key=JWT_SECRET,
            algorithms=["HS256"],
        )
        email = payload.get("email")
        if not email: raise credential_exception
    except jwt.InvalidTokenError:
        raise credential_exception

    query = select(model.User).where(model.User.email == email)
    res = await db.execute(query)
    user = res.scalar_one_or_none()
    if not user: raise credential_exception
    return user