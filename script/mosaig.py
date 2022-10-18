import sys
import glob
import numpy as np
import os
import psutil
import json
import datetime
import cv2
import torch
import tensorflow as tf

from rembg import remove
from glob import glob
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from keras.preprocessing import image
from scipy import spatial
from skimage import io
from utils import img_common_util




def test():
    imgselect = cv2.imread(selected_img)
    imgselect = cv2.cvtColor(imgselect, cv2.COLOR_BGR2RGB)
    tile_size = [50,50]
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
    im.save(selected_img)    

def saveLog():
    # Data to be written
    dictionary = {
        "id": iduser,
        "job": command,
        "date": str(datetime.datetime.now()),
        "folder": folder,
        "countfiles": len(All_files),
        "files": All_files
    }
     
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
     
    # Writing to sample.json
    dt = datetime.datetime.today()
    namefile = str(iduser)+""+str(dt.day)+""+str(dt.month)+""+str(dt.year)
    with open(str(namefile)+".json", "a+") as outfile:
        outfile.write(json_object)

    
#command in cmd
iduser = sys.argv[1]
selected_img = sys.argv[2] 
folder = sys.argv[3]
folder = folder+"/*"
All_files = glob(folder)

saveLog()
test()
