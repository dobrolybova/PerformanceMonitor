from uuid import UUID
import json
from pydantic import BaseModel, ValidationError, StrictStr


def get_uuid_if_valid(user_id: json) -> UUID:
    try:
        u_id = UUID(user_id["hash"])
    except (KeyError, ValueError, AttributeError):
        u_id = None
    return u_id


def validate_credentials(data: dict) -> bool:
    try:
        ValidateCredentials(**data)
    except ValidationError:
        return False
    return True


class ValidateCredentials(BaseModel):
    user: StrictStr
    passwd: StrictStr
