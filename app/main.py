from fastapi import FastAPI
app = FastAPI(title="First App", description="Build app for learning purpose")


#! uvicorn app.main:app --reload
@app.get("/")
def hello():

    return {"message": "hello world"}

