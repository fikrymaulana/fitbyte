from fastapi import UploadFile, File, HTTPException
from pathlib import Path
import imghdr, secrets
from fastapi import FastAPI
from fastapi.responses import JSONResponse


#bikin istance utama FastApi
app=FastAPI()

from fastapi.staticfiles import StaticFiles
import os

#pastikan folder uplaod selalu ada
os.makedirs("uploads", exist_ok=True)

#expose folder os uploads via url
app.mount("/uploads", StaticFiles(directory="uploads"),name="uploads")


@app.get("/",tags=['misc'], include_in_schema=True)
def hello_world():
    return JSONResponse({"message": "hello World tommy"})

ALLOWED_TYPES = {'image/jpeg', 'image/png'}
MAX_SIZE = 100 * 1024 #100kib

@app.post("/v1/file", tags=["file"])
async def upload_file(file: UploadFile=File(...)):
    #1) validasi content-type dari header
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only jpeg/jpg/png allowed")
    
    #2) baca konten dan cek ukuran
    content = await file.read()
    if len(content) > MAX_SIZE :
        raise HTTPException(status_code=400, detail="File too large (>100 KiB)")
    
    #3) validasi isi file (bukan sekedar ekstensi)
    kind = imghdr.what(None, h=content) #hasil = 'Jpeg'/ 'png' / 'jpg'/ none
    if kind not in {"jpeg", "jpg", "png"}:
        raise HTTPException(status_code=400, detail="invalide image data")
    
    #4) Tentukan ektesnsi & nama file aman/unik
    ext = "jpg" if kind == "jpeg" else "png"
    filename = f"{secrets.token_hex(8)}.{ext}"
    fpath = Path("uploads") / filename

    #5) simpan file 
    with open (fpath, "wb") as f:
        f.write(content)
    
    #6) balikan URL lokal untuk diakses
    url = f"http://localhost:8000/uploads/{filename}"
    return {"uri": url}