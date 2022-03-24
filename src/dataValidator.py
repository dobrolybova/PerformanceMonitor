from uuid import UUID


def get_uuid_if_valid(user_id) -> UUID:
    try:
        u_id = UUID(user_id["hash"])
    except (KeyError, ValueError, AttributeError):
        u_id = None
    return u_id

