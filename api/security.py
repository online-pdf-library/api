from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from api.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.auth.token_url)
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_ctx.verify(password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_ctx.hash(password)
