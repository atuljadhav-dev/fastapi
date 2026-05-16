from typing import Optional
from fastapi import FastAPI, status, Response
from pydantic import BaseModel, Field

app = FastAPI(title="First App", description="Build app for learning purpose")


#! uvicorn app.main:app --reload
@app.get("/")
def hello():

    return {"message": "hello world"}


@app.get("/user/{user_id}")
def get_user(user_id: int):  # user_id:int for validation of input parameter as integer
    return {"user_id": user_id}


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
    )
    email: str
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


@app.get("/header")
def header(response: Response):
    # use of header: rate limiting, versioning, authentication, etc.
    response.headers["X-App-Version"] = "1.1110"
    return {"message": "Header Added"}


@app.get("/login")
def login(response: Response):
    # use of cookie: session management, personalization, tracking, etc.
    response.set_cookie(
        key="token",
        value="Rahul",
        max_age=3600,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Cookie Added"}


@app.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logged Out"}
