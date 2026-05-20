from typing import Optional
from fastapi import FastAPI, status
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    HttpUrl,
    field_validator,
    model_validator,
    ConfigDict,
)
from app.response_model import res
from app.cookies import cookie
from app.headers import head
from app.file import files
from app.dependency import dep

app = FastAPI(title="First App", description="Build app for learning purpose")

app.include_router(dep, prefix="/dependency", tags=["Dependency"])
app.include_router(
    res, prefix="/response", tags=["Response"]
)  # tags are used to group the endpoints in the documentation
app.include_router(cookie, prefix="/auth", tags=["Cookie"])
app.include_router(head, prefix="/header", tags=["Header"])
app.include_router(files, prefix="/file", tags=["File"])


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
    gmail: EmailStr  # EmailStr is a Pydantic type that validates the email format.(EmailStr requires the email-validator package to be installed.)
    age: int = Field(
        ge=18, le=100, description="Age of the user", example=25
    )  # ge=18 means greater than or equal to 18 and le=100 means less than or equal to 100
    phone: list[int]
    address: Address
    marks: dict[str, float]  # marks is a dictionary with string keys and float values
    url: HttpUrl  # HttpUrl is a Pydantic type that validates the URL format.
    password: str = Field(
        min_length=8,
        max_length=20,
        description="Password of the user",
        example="P@ssw0rd",
    )  # min_length=8 means minimum length of 8 characters and max_length=20 means maximum length of 20 characters
    confirm_password: str = Field(
        min_length=8,
        max_length=20,
        description="Confirm Password of the user",
        example="P@ssw0rd",
    )

    @model_validator(
        mode="before"
    )  # Validate the password and confirm_password fields before the model is created
    def passwords_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        return values

    @model_validator(
        mode="after"
    )  # Validate the email field after the model is created
    def email_domain_check(self):
        email = self.email
        if email and not email.endswith("@example.com"):
            raise ValueError("Email must be from the domain example.com")
        return self

    @field_validator("name")
    @classmethod
    def name_must_be_alphabetic(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value

    @field_validator("name")
    @classmethod
    def capitalize_name(cls, value):
        return value.title()  # Capitalize the first letter of each word in the name


class UserResponse(BaseModel):
    email: str
    phone: list[int]
    name: str


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

# parameter priority: path > query > header > cookie > body
# best practise:
# Use path parameters to uniquely identify resources (e.g.,  /users/{user_id} ).
# Use query parameters for filtering, searching, sorting, and pagination (e.g.,  ?page=1&limit=10 ).
# Keep authentication tokens in the  Authorization  header rather than query parameters.
# Store session-related data in secure, HTTP-only cookies when appropriate.
# Add type hints to all parameters so FastAPI can validate them automatically.
# Avoid putting sensitive information such as passwords or API keys in URLs, since URLs are commonly logged and cached


# ConfigDict is a Pydantic class that allows you to configure the behavior of your Pydantic models. It can be used to set various options, such as whether to allow extra fields, whether to use aliases for field names, and whether to validate data on assignment.
class case1(BaseModel):
    model_config = ConfigDict(
        extra="allow"
    )  # extra="allow" means that extra fields are allowed in the model
    name: str
    age: int


class case2(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )  # extra="forbid" means that extra fields are not allowed in the model
    name: str
    age: int


class case3(BaseModel):
    model_config = ConfigDict(
        extra="ignore", validate_assignment=True, str_strip_whitespace=True
    )  # extra="ignore" means that extra fields are ignored in the model and validate_assignment=True means that the model will validate the data on assignment and str_strip_whitespace=True means that the model will strip whitespace from string fields on assignment
    name: str
    age: int
