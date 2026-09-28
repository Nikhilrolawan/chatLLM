from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as db:
        yield db