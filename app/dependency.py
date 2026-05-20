from fastapi import Depends, APIRouter, Header, HTTPException

dep = APIRouter()


def get_message():
    return "Hello Dependency"


def verify_token(authorization: str = Header(...)):
    if authorization != "Bearer secret":
        raise HTTPException(status_code=401, detail="Invalid Token")
    return {"username": "Rahul"}


@dep.get("/")
def home(message: str = Depends(get_message)):
    return {"message": message}


@dep.get("/protected")
def protected_route(user: dict = Depends(verify_token)):
    return {
        "message": f"Hello {user['username']}, you have access to this protected route."
    }


def get_database():
    return {"db": "my_database_connection"}


def get_repository(db: dict = Depends(get_database)):
    return {"repository": f"Repository connected to {db['db']}"}


def get_service(repo: dict = Depends(get_repository)):
    return {"service": f"Service using {repo['repository']}"}


@dep.get("/service")
def service_route(service: dict = Depends(get_service)):
    return {"message": f"Hello, this is the service route with {service['service']}"}
