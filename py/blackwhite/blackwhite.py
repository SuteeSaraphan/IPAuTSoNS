import sys
import datetime
import pymongo
import random
import string
from os import *
from glob import glob
from PIL import Image, ImageDraw, ImageFont

def BlackWhite():
    for x in range(len(All_files)):
        img = Image.open(All_files[x])
        imgGray = img.convert('L')
        imgGray.save(newfolder+"/"+All_files[x])

    
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
  BlackWhite()
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
