from fastapi import APIRouter, Response, Cookie

router = APIRouter()


@router.get("/login", tags=["auth","authentication"])  # tags are used to group the endpoints in the documentation
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


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logged Out"}


# cookie parameter
@router.get("/get-cookie")
def get_cookie(
    token: str | None = Cookie(default=None),
):  # Cookie parameter is used to retrieve the value of a cookie from the request. In this case, the function retrieves the value of the "token" cookie and returns it in the response. If the cookie is not present, the default value of None is returned.
    return {"token": token}
