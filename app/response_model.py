from fastapi import APIRouter,Response,Header
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse,
    JSONResponse,
)
res = APIRouter()


@res.get("/plain")
def get():
    return Response(content="hello", media_type="text/plain")


@res.get("/html")
def html():
    return HTMLResponse("""<h1>Welcome</h1><p>FastAPI HTML Response</p>""")


@res.get("/plaintext")
def plainText():
    return PlainTextResponse("hello")


@res.get("/redirect")
def redirect():
    return RedirectResponse("https://atuljadhav.tech")


def generate():
    for i in range(5):
        yield f"Line {i}\n"


@res.get("/stream")
def stream():
    return StreamingResponse(generate(), media_type="plain/text")


@res.get("/file")
def file():
    # display pdf in browser
    # FileResponse(path="Fastapi.pdf",filename="atul.pdf")
    return FileResponse("FastApi.pdf")


# Custom response
class SuccessResponse(JSONResponse):
    def __init__(self, data):
        super().__init__(content={"success": True, "data": data})


@res.get("/custom")
def custome():
    return SuccessResponse({"name": "Atul"})



