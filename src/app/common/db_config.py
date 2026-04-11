from sqlalchemy import URL
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL=settings.SQLALCHEMY_DATABASE_URI
async_engine= create_async_engine(DATABASE_URL,echo=False
                                  )
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """
    FastAPI dependency for providing database sessions to route handlers.

    This function serves as a dependency injection mechanism for FastAPI routes,
    providing a properly configured async database session. The session is
    automatically managed with proper cleanup through context management.

    Yields:
        AsyncSession: An async SQLAlchemy session for database operations.
                     The session is automatically closed when the request completes.

    Example:
        @app.get("/example")
        async def example_route(db: AsyncSession = Depends(get_db)):
            # Use db session for database operations
            pass
    """
    async with async_session() as session:
        yield session



async def init_db():
    """
    Initialize and test the database connection.

    This function performs a basic database connection test to ensure that
    the database is accessible and the connection configuration is correct.
    It's typically called during application startup to validate database
    connectivity before the application begins serving requests.

    The function creates a connection and runs a minimal operation to verify
    that the database engine is properly configured and operational.

    Raises:
        Exception: If the database connection cannot be established or
                  if there are configuration issues with the database engine.

    Example:
        # During application startup
        await init_db()
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda connection: None)