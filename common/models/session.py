from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from common.config import settings
# Database configuration

db_password = settings.POSTGRES_PASSWORD
db_user = settings.POSTGRES_USER
db_name = settings.POSTGRES_DB

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@db:5432/{db_name}"
DATABASE_ENGINE = create_async_engine(DATABASE_URL, echo=True, future=True)
DATABASE_ENGINE.conn

session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=DATABASE_ENGINE)

# not useful when using async senario instead handled manually
# SessionLocal = scoped_session(session_factory)

# Construct a base class for declarative class definitions
Base = declarative_base()

class DBSessionManager:

    def __init__(self) -> None:
        self._async_engine = DATABASE_ENGINE
        self._async_sessionmaker = session_factory

    async def close_async(self):
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._async_engine.dispose()
        
        self._async_engine = None
        self._async_sessionmaker = None


    @staticmethod
    @asynccontextmanager
    async def connect_async(self) -> AsyncIterator[AsyncConnection]:
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        #! Connect or begin ??????? 
        async with self._async_engine.connect() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session_async(self) -> AsyncIterator[AsyncSession]:
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        
        session = self._async_sessionmaker()
        try:
            yield session 
        except Exception:
            await session.rollback()
            raise
        finally:
            session.close()
    
    async def __aenter__(self) -> AsyncSession:
        return await self.session_async()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session_async().rollback()
        await self.session_async().close()

# Example of using the context manager to perform raw SQL queries
async def run_queries():
    async with DBSessionManager.connect_async() as connection:
        query = text("SELECT * FROM your_table")
        result = await connection.execute(query)
        rows = await result.fetchall()
        print(rows)
