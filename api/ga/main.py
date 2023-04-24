from fastapi import FastAPI, File, Response
from typing import Optional
import cv2
from segmentation import get_image_from_bytes
from engine import Engine
from animegan import AnimeGAN
import io
from PIL import Image
import numpy as np
import json
from collections import Counter
import io
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse



app = FastAPI(
    title="Ipautsons API GANModel Preview",
    description="""Ipautsons API GANModel Preview""",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:4070",
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


@app.post("/gan")
async def convert_image_to_ascii(file: bytes = File(...),modelse = "models/Shinkai_53.onnx",):
    input_image = get_image_from_bytes(file)
    input_image = np.array(input_image)
    animegan = AnimeGAN(modelse)
    engine = Engine(image_path=input_image, show=False,  custom_objects=[animegan])
    input_image = engine.run()

    

    pil_image = Image.fromarray(input_image)
    watermark = Image.open("watermark.png")
    width, height = pil_image.size
    w_width, w_height = watermark.size
    x = (width - w_width) // 2
    y = (height - w_height) // 2
    pil_image.paste(watermark, (x, y), watermark)

    # save PIL image to file buffer
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")

