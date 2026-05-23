from pydantic import BaseModel


class UserResponse(BaseModel):
    email: str
    phone: list[int]
    name: str
