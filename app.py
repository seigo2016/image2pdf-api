from email import header
from fastapi import FastAPI, UploadFile
import img2pdf
from PIL import Image
import os
from typing import List
from fastapi.responses import Response

app = FastAPI()


@app.post('/convert')
async def get_file(files: List[UploadFile]):
    data = []
    for f in files:
        if not (f.content_type == "image/jpeg" or f.content_type == "image/png"):
            return Response(status_code=400, content="Only jpeg and png files are allowed")
        
        d = await f.read()
        data.append(d)

    pdf_data = img2pdf.convert(data)
    headers = {
        'Content-Disposition': 'attachment; filename="test.pdf"'
    }

    return Response(content=pdf_data, headers=headers,  media_type="application/pdf")