from fastapi import FastAPI, status, Depends

from app.routers.response_model import router as response_router
from app.routers.cookies import router as cookie_router
from app.routers.headers import router as head_router
from app.routers.file import router as files_router
from app.routers.dependency import router as dep_router

from app.schemas.UserResponse import UserResponse
from app.schemas.User import User


from app.dependencies.log_request_data import log_request_data

app = FastAPI(
    title="First App",
    description="Build app for learning purpose",
    dependencies=[Depends(log_request_data)],
)  # dependencies are used to add global dependencies to the app, so that all endpoints will require the token verification

app.include_router(dep_router)
app.include_router(
    response_router, prefix="/response", tags=["Response"]
)  # tags are used to group the endpoints in the documentation
app.include_router(cookie_router, prefix="/auth", tags=["Cookie"])
app.include_router(head_router, prefix="/header", tags=["Header"])
app.include_router(files_router, prefix="/file", tags=["File"])


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
