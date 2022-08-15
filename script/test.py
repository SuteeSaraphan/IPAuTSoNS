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
from models.module_photo2pixel import Photo2PixelModel
from utils import img_common_util




def test(number):
    if number == "1":#black white
        for x in range(len(All_files)):
            img = Image.open(All_files[x])
            imgGray = img.convert('L')
            imgGray.save(All_files[x])
    elif number == "2":#ascii
        for x in range(len(All_files)):
            SC = 0.1    # pixel sampling rate in width
            GCF= 2 
            color1='black'
            color2='blue'
            bgcolor='white'
            img = Image.open(All_files[x])
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

            # Save the image file

            #out_f = out_f.resize((1280,720))
            #can't jpg
            out_f = All_files[x]
            newImg.save(out_f)
    elif number == "3":#mosaig
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
    elif number == "4":#pixelart
        for x in range(len(All_files)):
            image = Image.open(All_files[x])
            imageinput = All_files[x]
            output = All_files[x]
            kernel_size = 10
            pixel_size = 16
            edge_thresh = 100

            img_input = Image.open(imageinput)
            img_pt_input = img_common_util.convert_image_to_tensor(img_input)

            model = Photo2PixelModel()
            model.eval()
            with torch.no_grad():
                img_pt_output = model(
                    img_pt_input,
                    param_kernel_size=kernel_size,
                    param_pixel_size=pixel_size,
                    param_edge_thresh=edge_thresh
                )
            img_output = img_common_util.convert_tensor_to_image(img_pt_output)
            img_output.save(output)
    elif number == "5":#bgremove
        for x in range(len(All_files)):
            img = cv2.imread(All_files[x])
            output = remove(img)
            cv2.imwrite(All_files[x]+".png", output)
            os.remove(All_files[x])
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
command = sys.argv[2] 
folder = sys.argv[3]
if len(sys.argv) >= 5:
  selected_img = sys.argv[4]
folder = folder+"/*"
All_files = glob(folder)

saveLog()
# Getting % usage of virtual_memory ( 3rd field)
#print('The CPU usage is: ', psutil.cpu_percent(0))
#print('RAM memory % used:', psutil.virtual_memory()[2])
test(command)
# Getting % usage of virtual_memory ( 3rd field)
print('The CPU usage is: ', psutil.cpu_percent(0))
print('RAM memory % used:', psutil.virtual_memory()[2])