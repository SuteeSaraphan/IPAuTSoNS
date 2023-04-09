import random
import string
import pymongo
import os
from os import *

client = pymongo.MongoClient(
    "mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons

img_file_col = db['api_image_file']
folder_img_col = db['api_folder_img']

user_id = "p5mltrbi9ar" #user ownner of this image
img_folder = "test_processed" #folder name of image
folder_path ="IPAutSoNsAPI/yaml_file"#path to folder

folder_data = {
                'folder_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
                'user_id_id': user_id,
                'folder_name': img_folder,
                'path': folder_path+"/"+img_folder,
                'is_hidden': False
            }

try:
    result = folder_img_col.insert_one(folder_data)
    print(result)
except Exception as error:
    print(error)

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
                'path': folder_path+"/"+i,
                'img_size': str(file_size)
                }

    list_add_db.append(dict_temp)
    
try:
    result = img_file_col.insert_many(list_add_db)
    print(result)
except Exception as error:
    print(error)