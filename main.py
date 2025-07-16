from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import time
from test_by_onnx import Convert

app = FastAPI()

UPLOAD_DIR = "inputs/"
OUTPUT_DIR = "output/"
MODEL_PATH = "AnimeGANv3_Hayao_36.onnx"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory store for tracking client timeouts
client_request_log = {}  # Format: {ip: [last_request_time, fail_count]}


def get_client_ip(request: Request) -> str:
    return request.client.host


def enforce_exponential_timeout(ip: str):
    now = time.time()
    last_info = client_request_log.get(ip, [0, 0])
    last_time, fail_count = last_info

    wait_time = 2 ** fail_count  # Exponential backoff: 1s, 2s, 4s, 8s, etc.

    if now - last_time < wait_time:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Please wait {round(wait_time - (now - last_time), 2)} seconds.",
        )

    # Update fail count or reset
    if now - last_time > 60:
        # Reset after 1 min of no requests
        client_request_log[ip] = [now, 0]
    else:
        client_request_log[ip] = [now, fail_count + 1]


@app.post("/stylize/")
async def stylize_image(
    request: Request,
    file: UploadFile = File(...),
    device: str = Form("cpu")
):
    ip = get_client_ip(request)
    enforce_exponential_timeout(ip)

    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    upload_path = os.path.join(UPLOAD_DIR, filename)

    # Save the uploaded image
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run the ONNX model
    Convert(input_img_path=upload_path, output_path=OUTPUT_DIR, onnx=MODEL_PATH, device=device)

    # Path to stylized image
    output_path = os.path.join(OUTPUT_DIR, filename)

    return FileResponse(output_path, media_type="image/jpeg", filename=f"stylized_{file.filename}")
