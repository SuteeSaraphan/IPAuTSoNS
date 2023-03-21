from fastapi import FastAPI, File
from segmentation import get_image_from_bytes
from starlette.responses import Response
import io
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from collections import Counter
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
import sys
import numpy as np
import os
import datetime
import psutil
import torch

from models.module_photo2pixel import Photo2PixelModel

from numpy import load
from numpy import expand_dims

def convert_image_to_tensor(img):
    img = img.convert("RGB")
    img_np = np.array(img).astype(np.float32)
    img_np = np.transpose(img_np, axes=[2, 0, 1])[np.newaxis, :, :, :]
    img_pt = torch.from_numpy(img_np)
    return img_pt


def convert_tensor_to_image(img_pt):
    img_pt = img_pt[0, ...].permute(1, 2, 0)
    result_rgb_np = img_pt.cpu().numpy().astype(np.uint8)
    return Image.fromarray(result_rgb_np)


app = FastAPI(
    title="API ipautsons Basic App",
    description="""Basic App""",
    version="1.0.2",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
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




@app.post("/pixelart")
async def convert_image_to_pixelart(file: bytes = File(...)):
    img_input = get_image_from_bytes(file)
    kernel_size = 8
    pixel_size = 16
    edge_thresh = 70
    img_pt_input = convert_image_to_tensor(img_input)
    model = Photo2PixelModel()
    model.eval()
    with torch.no_grad():
        img_pt_output = model(
            img_pt_input,
            param_kernel_size=kernel_size,
            param_pixel_size=pixel_size,
            param_edge_thresh=edge_thresh
        )
    img_output = convert_tensor_to_image(img_pt_output)
    watermark = Image.open("watermark.png")
    width, height = img_output.size
    w_width, w_height = watermark.size
    x = (width - w_width) // 2
    y = (height - w_height) // 2
    img_output.paste(watermark, (x, y), watermark)
    buffer = BytesIO()
    img_output.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    # Return the image as a response
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")

@app.post("/blackwhite")
async def convert_image_to_blackwhite(file: bytes = File(...)):
    img = get_image_from_bytes(file)
    imgGray = img.convert('L')

    watermark = Image.open("watermark.png")
    width, height = imgGray.size
    w_width, w_height = watermark.size
    x = (width - w_width) // 2
    y = (height - w_height) // 2
    imgGray.paste(watermark, (x, y), watermark)

    buffer = BytesIO()
    imgGray.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()
    # Return the image as a response
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")

@app.post("/ascii")
async def convert_image_to_ascii(file: bytes = File(...)):
    img = get_image_from_bytes(file)
    SC = 0.1
    GCF= 2 
    color1='black'
    color2='blue'
    bgcolor='white'
    chars = np.asarray(list(' .,:irs?@9B&#'))
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    WCF = letter_height/letter_width
    widthByLetter=round(img.size[0]*SC*WCF)
    heightByLetter = round(img.size[1]*SC)
    S = (widthByLetter, heightByLetter)
    img = img.resize(S)
    img = np.sum(np.asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img/img.max())**GCF*(chars.size-1)
    lines = ("\n".join( ("".join(r) for r in chars[img.astype(int)]) )).split("\n")
    nbins = len(lines)
    newImg_width= letter_width *widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGB", (newImg_width, newImg_height), bgcolor)
    draw = ImageDraw.Draw(newImg)
    leftpadding=0
    y = 0
    lineIdx=0
    for line in lines:
        color = 'blue'
        lineIdx +=1
        draw.text((leftpadding, y), line, '#0000FF', font=font)
        y += letter_height

    watermark = Image.open("watermark.png")
    width, height = newImg.size
    w_width, w_height = watermark.size
    x = (width - w_width) // 2
    y = (height - w_height) // 2
    newImg.paste(watermark, (x, y), watermark)    
    # Convert the image to bytes
    buffer = BytesIO()
    newImg.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    # Return the image as a response
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")

