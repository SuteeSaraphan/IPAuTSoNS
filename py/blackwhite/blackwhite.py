import sys
import datetime
import pymongo
import random
import string
import os
from os import *
from glob import glob
from PIL import Image, ImageDraw, ImageFont

def BlackWhite():
    for x in range(len(All_files)):
        img = Image.open(All_files[x])
        imgGray = img.convert('L')
        filename, extension = os.path.splitext(os.path.basename(All_files[x]))
        imgGray.save(newfolder+"/"+filename+extension)

    
#command in cmd
job_id = sys.argv[1]
useridparam = sys.argv[2]
job = None
folder = sys.argv[3]
newfolder = sys.argv[4]
folder = folder+"/*"
All_files = glob(folder+'.png') + glob(folder+'.PNG') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.JPG') + glob(folder+'.JPEG') + glob(folder+'.tiff') + glob(folder+'.TIFF')


client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons
try:
    job = db.api_job.find_one({'job_id' : job_id})
except NameError as error:
    job = None

try:
    BlackWhite()
    print("done")
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
    print("An exception occurred")
    if job != None and type(job) == dict:
        job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                        {"$set":
                                                            {'job_status' : 2
                                                            }
                                                        },upsert=True)

