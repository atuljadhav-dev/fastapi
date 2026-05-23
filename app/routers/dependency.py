from fastapi import Depends, APIRouter, Header, HTTPException
from app.dependencies.api_router_dependency import api_router_dependency
from app.dependencies.get_message import get_message
from app.dependencies.verify_token import verify_token
router = APIRouter(
    prefix="/dependency",
    dependencies=[Depends(api_router_dependency)],
    tags=["Dependency"],
)


@router.get("/")
def home(
    message: str = Depends(get_message), msg: str = Depends(get_message)
):  # without use_cache=False, the second call will use the cached value from the first call
    return {"message": message, "msg": msg}


@router.get("/hello")
def home(
    message: str = Depends(get_message),
    msg: str = Depends(
        get_message, use_cache=False
    ),  # without use_cache=False, the second call will use the cached value from the first call
):
    return {"message": message, "msg": msg}


@router.get("/protected")
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


@router.get("/service")
def service_route(service: dict = Depends(get_service)):
    return {"message": f"Hello, this is the service route with {service['service']}"}
