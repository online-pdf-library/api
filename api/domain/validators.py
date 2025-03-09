import typing
from datetime import datetime

import pytz
from pydantic import AfterValidator, ValidationInfo

from api.config import config


def validate_timezone(v: str, _: ValidationInfo) -> str:
    try:
        return str(pytz.timezone(zone=v))
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Unknown timezone '{v}'") from None


Timezone = typing.Annotated[str, AfterValidator(validate_timezone)]


def validate_datetime(v: datetime | None, _: ValidationInfo) -> datetime | None:
    if v is None:
        return None
    if v.tzinfo is None:
        return v.replace(tzinfo=pytz.utc)
    return v.astimezone(tz=pytz.utc)


Datetime = typing.Annotated[datetime, AfterValidator(validate_datetime)]
OptionalDatetime = typing.Annotated[datetime, AfterValidator(validate_datetime)]


def validate_password(v: str) -> str:
    v = v.strip()

    if len(v) < config.password.min_len:
        raise ValueError(f"Password is too short ({len(v)} < {config.password.min_len}).")
    if len(v) > config.password.max_len:
        raise ValueError(f"Password is too long ({len(v)} > {config.password.max_len}).")
    for c in v:
        if c not in config.password.allowed_characters:
            raise ValueError(f"Password contains illegal character '{c}'.")

    return v


Password = typing.Annotated[str, AfterValidator(validate_password)]
