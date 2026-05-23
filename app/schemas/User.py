from typing import Optional

from pydantic import BaseModel, BaseModel, Field, EmailStr, HttpUrl, field_validator, model_validator, ConfigDict


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
