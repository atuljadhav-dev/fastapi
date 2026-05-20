from fastapi import APIRouter, File, HTTPException, UploadFile, Form
import shutil
import os

# need package: pip install python-multipart
files = APIRouter()


@files.post("/upload")
async def upload_file(name: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()  # read the content of the uploaded file
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content.decode("utf-8"),
        "name": name,
    }


@files.post("/upload-multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    if len(files) > 5:
        raise HTTPException(
            status_code=400, detail="You can upload a maximum of 5 files."
        )
    filenames = []
    for file in files:
        filenames.append(file.filename)
    return {"files": filenames}


@files.post("/upload-save")
async def upload_file_save(file: UploadFile = File(...)):
    with open(f"uploaded_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": f"File '{file.filename}' saved successfully."}


@files.post("/validate-upload")
async def validate_upload(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in [".txt", ".pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .txt and .pdf files are allowed.",
        )
    if file.content_type not in ["text/plain", "application/pdf"]:
        # common MIME types image/jpeg, image/png,image/gif, application/pdf, text/plain,application/json,
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only text and PDF files are allowed.",
        )
    # size validation (e.g., max 1MB)
    file_size = await file.read()
    if file_size > 1 * 1024 * 1024:  # 1MB
        raise HTTPException(
            status_code=400, detail="File size exceeds the maximum limit of 1MB."
        )
    file.seek(0)  # Reset the file pointer to the beginning
    return {"filename": file.filename, "content_type": file.content_type}
