from fastapi import FastAPI, File, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from zipfile import ZipFile
import os

app = FastAPI(
    title="API ipautsons zip",
    description="""zip App""",
    version="1.0.2",
)

origins = [
    "http://localhost",
    "http://localhost:4090",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return dict(msg='OK')



@app.get("/downloadzip")
async def download_files(path="path"):
    # Define the folder containing the files to be zipped
    folder = path
    
    # Create a zip file from the folder
    with ZipFile("files.zip", "w") as zip:
        for file in os.listdir(folder):
            zip.write(os.path.join(folder, file), file)

    # Read the contents of the zip file into a bytes object
    with open("files.zip", "rb") as f:
        content = f.read()

    # Return a Response object with the bytes as the response content
    response = Response(content=content, media_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=files.zip"
    return response

