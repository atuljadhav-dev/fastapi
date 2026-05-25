from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id == 0:
        raise UserNotFoundException(user_id)
    return {"user_id": user_id}


class UserNotFoundException(Exception):
    """Custom exception for when a user is not found."""

    def __init__(self, user_id: int):
        self.user_id = user_id
