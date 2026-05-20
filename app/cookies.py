from fastapi import APIRouter, Response, Cookie

cookie = APIRouter()


@cookie.get("/login")
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


@cookie.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logged Out"}


# cookie parameter
@cookie.get("/get-cookie")
def get_cookie(token: str | None = Cookie(default=None)): # Cookie parameter is used to retrieve the value of a cookie from the request. In this case, the function retrieves the value of the "token" cookie and returns it in the response. If the cookie is not present, the default value of None is returned.
    return {"token": token}
