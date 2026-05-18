from fastapi import APIRouter, Response
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
