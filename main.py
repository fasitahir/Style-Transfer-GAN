from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import sys
sys.path.append(os.path.abspath("GAN-V2/GAN-V2/deploy"))
from test_by_onnx import Convert

app = FastAPI()


UPLOAD_DIR = "inputs/"
OUTPUT_DIR = "output/"
MODEL_PATH = "AnimeGANv3_Hayao_36.onnx"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/stylize/")
async def stylize_image(file: UploadFile = File(...), device: str = Form("cpu")):
    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    upload_path = os.path.join(UPLOAD_DIR, filename)

    # Save the uploaded image
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run the ONNX model
    Convert(input_imgs_path=UPLOAD_DIR, output_path=OUTPUT_DIR, onnx=MODEL_PATH, device=device)

    # Path to stylized image
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Return the stylized image
    return FileResponse(output_path, media_type="image/jpeg", filename=f"stylized_{file.filename}")
