import typing
from datetime import timedelta

from pydantic import AfterValidator, BaseModel, Field, ValidationInfo
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def build_db_url(_: str, info: ValidationInfo) -> str:
    db: DBConfig = info.data["db"]
    db_url = MultiHostUrl.build(
        scheme=db.driver,
        username=db.username,
        password=db.password,
        host=db.host,
        port=db.port,
        path=db.dbname,
    )
    return str(db_url)


class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    token_url: str = Field(default="sign-in")
    token_expire: timedelta = timedelta(minutes=30)


class AppConfig(BaseModel):
    host: str
    port: int
    reload: bool


class DBConfig(BaseModel):
    driver: str
    username: str
    password: str
    host: str
    port: int
    dbname: str


class PaginationConfig(BaseModel):
    min_page_size: int = 5
    max_page_size: int = 100
    default_page_size: int = 25


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    app: AppConfig = Field(default=...)

    db: DBConfig = Field(default=...)
    db_url: typing.Annotated[str, AfterValidator(build_db_url)] = ""

    pagination: PaginationConfig = PaginationConfig()

    auth: AuthConfig = Field(default=...)


config = Config()
