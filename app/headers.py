from fastapi import Header, APIRouter, Response

head = APIRouter()


@head.get("/profile")
def profile(authorization: str = Header()):
    return {"token": authorization}


@head.get("/header")
def header(response: Response):
    # use of header: rate limiting, versioning, authentication, etc.
    response.headers["X-App-Version"] = "1.1110"
    return {"message": "Header Added"}


@head.get("/laguages")
def laguages(accept_language: str | None = Header(default=None)):
    return {"accept_language": accept_language}

@head.get("/convert")
def con(accept_language: str = Header(convert_underscores=False)):# convert_underscores=False is used to prevent FastAPI from converting underscores to hyphens in the header name. By default, FastAPI converts underscores to hyphens in header names, which can cause issues when working with certain headers that contain underscores.
    return {"accept_language": accept_language}