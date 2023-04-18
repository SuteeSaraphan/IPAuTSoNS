import random
import string
import pymongo
import os
from os import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

client = pymongo.MongoClient(
    "mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons

img_file_col = db['api_image_file']


user_id = "p5mltrbi9ar" #user ownner of this image
img_folder = "test_processed" #folder name of image
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