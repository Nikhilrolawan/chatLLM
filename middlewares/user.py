import asyncio
import jwt
import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

def user_middleware(authorization: str = Header()):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing auth headers"
        )
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )
        decoded = jwt.decode(
            jwt = token,
            key=JWT_SECRET,
            algorithms=["HS265"],
        )
        return decoded
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=403,
            detail="Invalid Credentials",
        )
