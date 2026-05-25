from fastapi import Header, HTTPException
def verify_token(authorization: str = Header(...)):
    if authorization != "Bearer secret":
        raise HTTPException(status_code=401, detail="Invalid Token")
    return {"username": "Rahul"}
