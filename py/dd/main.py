from fastapi import FastAPI, File
from segmentation import get_image_from_bytes
from starlette.responses import Response
import io
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
import numpy as np
import psutil
import torch

from models.module_photo2pixel import Photo2PixelModel

from numpy import load
from numpy import expand_dims
from numpy import shape

import glob
import tensorflow as tf

from glob import glob
from keras.preprocessing import image
from scipy import spatial
from utils import img_common_util

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
    version="1.0.3",
)

origins = [
    "http://localhost",
    "http://localhost:4020",
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

@app.post("/mosaig")
async def convert_image_to_mosaig(file: bytes = File(...), folders = ""):
    imgselect = get_image_from_bytes(file)
    folder = folders+"/*"
    All_files = glob(folder+'.png') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.tiff')
    tile_size = [5,5]
    imgselect = np.array(imgselect)
    h,w,c = imgselect.shape
    h_tile = int(h/tile_size[0])
    w_tile = int(w/tile_size[1])
    tile = np.zeros((h_tile,w_tile,c))
    for i in range(h_tile):
        for j in range(w_tile):
            tile[i,j] = np.mean(imgselect[i*tile_size[0] : (i+1)*tile_size[0] , j*tile_size[1]: (j+1)*tile_size[1],:],axis=(0,1))
    image_feature = tile.astype(dtype=np.uint8)
    tile.astype(dtype=np.uint8)

    # Load tile images and resize to tile_size
    tile = tf.keras.utils.load_img(target_size=tile_size,path =All_files[0],color_mode='rgb')
    tiles = []
    for i in range(len(All_files)):
            tile = tf.keras.utils.load_img(target_size=tile_size,path =All_files[i],color_mode='rgb')
            tiles.append(np.array(tile))
    Tile_features = []
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=(0,1))
        Tile_features.append(mean_color)
    h_tiles = int(imgselect.shape[0]/tile_size[0])
    w_tiles = int(imgselect.shape[1]/tile_size[1])

    tree = spatial.KDTree(Tile_features)
    closet_tiles = np.zeros((h_tiles,w_tiles))
    for h in range(h_tiles):
        for w in range(w_tiles):
            closet = tree.query(image_feature[h,w])
            closet_tiles[h,w] = np.array(closet[1])
    # Fill each subimage with matched tile
    # Offset of tile
    main_image2 = imgselect.copy()
    main_photo = imgselect

    for h in range(image_feature.shape[0]):
        for w in range(image_feature.shape[1]):
            h_tile,y_tile = h*tile_size[0], w*tile_size[1]
            # Index of tile
            index = closet_tiles[h,w]
            main_photo[h_tile:int(h_tile+tile_size[0]), y_tile:(y_tile+tile_size[1]),:] = tiles[int(index)]
    im = Image.fromarray(imgselect)
    buffer = BytesIO()

    watermark = Image.open("watermark.png")
    width, height = im.size
    w_width, w_height = watermark.size
    x = (width - w_width) // 2
    y = (height - w_height) // 2
    im.paste(watermark, (x, y), watermark)    
    # Convert the image to bytes
    buffer = BytesIO()
    im.save(buffer, format="JPEG")
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

