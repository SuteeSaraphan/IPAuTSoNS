import sys
import glob
import numpy as np
import os
import psutil
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

client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons
try:
    job = db.api_job.find_one({'job_id' : job_id})
except NameError as error:
    job = None
try:
    test()
    if job != None and type(job) == dict:
        job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                        {"$set":
                                                            {'job_status' : 1
                                                            }
                                                        },upsert=True)
        img_file_col = db['api_image_file']


    user_id = useridparam #user ownner of this image
    img_folder = newfolder #folder name of image
    folder_path = os.path.join("ipautsons", user_id, "root", img_folder) #path of image folder
    path_for_add_db = img_folder.split("/")[-3:]
    onlyfiles = listdir(folder_path)
    list_add_db = []
    for i in onlyfiles:
        dict_temp = {}
        img_type = "image/"+i.split('.')[-1]
        file_size = os.path.getsize(folder_path+"/"+i)

        dict_temp = {
                    'img_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                    'user_id_id': user_id,
                    'img_type': img_type,
                    'img_folder': img_folder.split("/")[-1],
                    'path': path_for_add_db[0]+"/"+path_for_add_db[1]+"/"+path_for_add_db[2]+"/"+i,
                    'img_size': str(file_size)
                    }

        list_add_db.append(dict_temp)

    try:
        result = img_file_col.insert_many(list_add_db)
        print(result)
    except Exception as error:
        print(error)
except:
  print("An exception asd")
  if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 2
                                                        }
                                                    },upsert=True)
