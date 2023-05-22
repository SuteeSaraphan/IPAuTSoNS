import sys
import glob
import numpy as np
import os
import psutil
import pymongo
import datetime
import cv2
import tensorflow as tf
import random
import string
from os import *

from glob import glob
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont
from keras.preprocessing import image
from scipy import spatial
from utils import img_common_util




def test():
    imgselect = cv2.imread(selected_img)
    imgselect = cv2.cvtColor(imgselect, cv2.COLOR_BGR2RGB)
    tile_size = [5,5]
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
    filename, extension = os.path.splitext(os.path.basename(selected_img))
    im.save(newfolder+"/"+filename+extension)



    
#command in cmd
job_id = sys.argv[1]
useridparam = sys.argv[2]
job = None
folder = sys.argv[3]
selected_img = sys.argv[4]
newfolder = sys.argv[5]
folder = folder+"/*"
All_files = glob(folder+'.png') + glob(folder+'.PNG') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.JPG') + glob(folder+'.JPEG') + glob(folder+'.tiff') + glob(folder+'.TIFF') 


print(All_files)
test()
