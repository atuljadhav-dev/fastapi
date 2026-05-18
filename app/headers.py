
from fastapi import Header,APIRouter,Response
head = APIRouter()


@head.get("/profile")
def profile(authorization: str = Header()):
    return {"token": authorization}

@head.get("/header")
def header(response: Response):
    # use of header: rate limiting, versioning, authentication, etc.
    response.headers["X-App-Version"] = "1.1110"
    return {"message": "Header Added"}