import sys
import glob
import numpy as np
import os
import json
import datetime
import pymongo
import random
import string

from glob import glob
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont
from os import *


def ASCII():
    for x in range(len(All_files)):
        SC = 0.1
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
        filename, extension = os.path.splitext(os.path.basename(out_f))
        newImg.save(newfolder+"/"+filename+extension)

#command in cmd
job_id = sys.argv[1]
useridparam = sys.argv[2]
job = None
folder = sys.argv[3]
newfolder = sys.argv[4]

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
    ASCII()
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
                    'path': img_folder+"/"+i,
                    'img_size': str(file_size)
                    }

        list_add_db.append(dict_temp)

    try:
        result = img_file_col.insert_many(list_add_db)
        print(result)
    except Exception as error:
        print(error)
except Exception as error:
  print("error because : "+str(error))
  if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 2
                                                        }
                                                    },upsert=True)



