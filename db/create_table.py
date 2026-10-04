import os
import asyncio

from models.model import Base
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add it to chatllm/.env")


async def main():
    async_engine = create_async_engine(DATABASE_URL)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())