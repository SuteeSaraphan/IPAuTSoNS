import sys
import glob
import numpy as np
import os
import psutil
import json
import datetime
import torch
import pymongo
import random
import string
from os import *
from glob import glob
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from models.module_photo2pixel import Photo2PixelModel


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



def test():
    for x in range(len(All_files)):
        image = Image.open(All_files[x])
        imageinput = All_files[x]
        output = All_files[x]
        kernel_size = 10
        pixel_size = 16
        edge_thresh = 100

        img_input = Image.open(imageinput)
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
        img_output.save(newfolder+"/"+output)
 
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

job_id = sys.argv[1]
useridparam = sys.argv[2]
job = None
folder = sys.argv[3]
newfolder = sys.argv[4]
folder = folder+"/*"
All_files = glob(folder+'.png') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.tiff')  


client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons
try:
    job = db.api_job.find_one({'job_id' : job_id})
except NameError as error:
    job = None

try:
  test()
  print("done")
  if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 1
                                                        }
                                                    },upsert=True)
    client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
    db = client.ipautsons

    img_file_col = db['api_image_file']


    user_id = useridparam #user ownner of this image
    img_folder = newfolder #folder name of image
    folder_path = os.path.join("ipautsons", user_id, "root", img_folder) #path of image folder


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
                    'img_folder': img_folder,
                    'path': user_id+"/root/"+img_folder+"/"+i,
                    'img_size': str(file_size)
                    }

        list_add_db.append(dict_temp)

    try:
        result = img_file_col.insert_many(list_add_db)
        print(result)
    except Exception as error:
        print(error)
except:
  print("An exception occurred")
  if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 2
                                                        }
                                                    },upsert=True)

