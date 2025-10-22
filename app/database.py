from datetime import datetime
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .config import settings

DB_URL = settings.db_url
engine = create_async_engine(DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

str_pk = Annotated[str, mapped_column(primary_key=True)]
int_pk = Annotated[int, mapped_column(primary_key=True)]
time_created = Annotated[datetime, mapped_column(server_default=func.now())]
time_updated = Annotated[datetime, mapped_column(onupdate=func.now())]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    time_created: Mapped[time_created]
    time_updated: Mapped[time_updated]


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper
