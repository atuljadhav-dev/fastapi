from typing import Optional
from fastapi import FastAPI, status, Response
from pydantic import BaseModel, Field
from app.response_model import res
from app.cookies import cookie
from app.headers import head
app = FastAPI(title="First App", description="Build app for learning purpose")

app.include_router(res, prefix="/response", tags=["Response"])
app.include_router(cookie, prefix="/auth", tags=["Cookie"])
app.include_router(head, prefix="/header", tags=["Header"])

#! uvicorn app.main:app --reload
@app.get("/")
def hello():
    return {"message": "hello world"}


# path parameter
@app.get("/user/{user_id}")
def get_user(user_id: int):  # user_id:int for validation of input parameter as integer
    return {"user_id": user_id}


# path+query parameter
@app.get("/users/{userId}")
def get_user(userId: int, active: bool = True):
    # /users/345?active=true
    # /users/345 uses ture default value
    return {"userId": userId, "active": active}


class Address(BaseModel):
    city: Optional[str] = None  # Optional field with a default value of None
    state: str
    pincode: int


class User(BaseModel):
    name: str = Field(
        min_length=3, max_length=50, description="Name of the user", example="John Doe"
    )  # Field is used to add validation and metadata to the name field, such as minimum and maximum length, description, and example value
    email: str = Field(
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Email of the user",
        example="john.doe@example.com",
    )
    phone: list[int]
    address: Address
    marks: dict[str, float]  # marks is a dictionary with string keys and float values


class UserResponse(BaseModel):
    email: str
    phone: list[int]


@app.post(
    "/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)  # response_model is used to filter the response data and return only the fields defined in the UserResponse model and status_code=status.HTTP_201_CREATED means that the request was successful and a new resource was created
def create_user(user: User):
    return user


# status.HTTP_200_OK
# status.HTTP_201_CREATED
# status.HTTP_204_NO_CONTENT
# status.HTTP_400_BAD_REQUEST
# status.HTTP_401_UNAUTHORIZED
# status.HTTP_403_FORBIDDEN
# status.HTTP_404_NOT_FOUND
# status.HTTP_422_UNPROCESSABLE_ENTITY
# status.HTTP_500_INTERNAL_SERVER_ERROR