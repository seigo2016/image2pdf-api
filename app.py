from ast import Bytes
from fastapi import FastAPI, UploadFile, File
from starlette.middleware.cors import CORSMiddleware
import img2pdf
from typing import List
from fastapi.responses import Response
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["get","post"],
    allow_headers=["*"]
)

@app.post('/convert')
async def get_file(filename: str="default.pdf", files: List[UploadFile] =  File(...)) -> Response:
    if not filename.endswith(".pdf"):
        filename = filename + ".pdf"
    data: List[Bytes] = []
    for f in files:
        if not (f.content_type == "image/jpeg" or f.content_type == "image/png"):
            return Response(status_code=400, content="Only jpeg and png files are allowed")
        
        d = await f.read()
        data.append(d)

    pdf_data:Bytes = img2pdf.convert(data)

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return Response(content=pdf_data, headers=headers,  media_type="application/pdf")