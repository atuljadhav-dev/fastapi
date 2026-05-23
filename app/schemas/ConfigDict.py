from pydantic import BaseModel, ConfigDict


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
