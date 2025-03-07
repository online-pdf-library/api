from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.config import config

engine = create_async_engine(url=config.db_url, echo=False)
Session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
