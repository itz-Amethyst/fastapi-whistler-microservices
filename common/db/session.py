from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Union
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, Session

from common.config import settings
# Database configuration

db_password = settings.POSTGRES_PASSWORD
db_user = settings.POSTGRES_USER
db_name = settings.POSTGRES_DB

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@db:5432/{db_name}"
DATABASE_ENGINE_ASYNC = create_async_engine(DATABASE_URL, echo=True, future=True)
DATABASE_ENGINE = create_engine(DATABASE_URL.replace("postgresql+asyncpg", "postgresql"), echo=True, future=True)

MetaData = MetaData()

session_factory_async = async_sessionmaker(autocommit=False, bind=DATABASE_ENGINE_ASYNC, expire_on_commit=False)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=DATABASE_ENGINE_ASYNC)

# not useful when using async senario instead handled manually
# SessionLocal = scoped_session(session_factory)

# Construct a base class for declarative class definitions
Base = declarative_base()

# Supports both async and sync
class DBSessionManager:

    def __init__(self) -> None:
        self._async_engine = DATABASE_ENGINE_ASYNC
        self._async_sessionmaker = session_factory_async
        self._sync_engine = DATABASE_ENGINE
        self._sync_sessionmaker = session_factory

    async def close_async(self):
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._async_engine.dispose()
        
        self._async_engine = None
        self._async_sessionmaker = None

    def close_sync(self):
        if self._sync_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self._sync_engine.dispose()

    @staticmethod
    @asynccontextmanager
    async def connect_async(self) -> AsyncIterator[AsyncConnection]:
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        #! Connect or begin ??????? 
        async with self._async_engine.begin() as connection:
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
    @contextmanager
    def session_sync(self):
        if self._sync_sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        
        session = self._sync_sessionmaker
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def __enter__(self) -> Union[Session, AsyncSession]:
        return self.session_sync()    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session_sync().rollback()
        self.session_sync.close()

    async def __aenter__(self) -> AsyncSession:
        return await self.session_async()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session_async().rollback()
        await self.session_async().close()


sessionManager = DBSessionManager()

async def get_db_session_async():
    async with sessionManager.session_async() as session:
        yield session


def get_db_session_sync():
    with sessionManager.session_sync() as session:
        yield session

# Example of using the context manager to perform raw SQL queries
async def run_queries():
    async with DBSessionManager.connect_async() as connection:
        query = text("SELECT * FROM your_table")
        result = await connection.execute(query)
        rows = await result.fetchall()
        print(rows)
