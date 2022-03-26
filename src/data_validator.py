from uuid import UUID
import json
import dataclasses


def get_uuid_if_valid(user_id: json) -> UUID:
    try:
        u_id = UUID(user_id["hash"])
    except (KeyError, ValueError, AttributeError):
        u_id = None
    return u_id


def validate_credentials(data: dict) -> bool:
    try:
        ValidateCredentials(**data)
    except TypeError:
        return False
    return True


@dataclasses.dataclass
class ValidateCredentials:
    user: str
    passwd: str
