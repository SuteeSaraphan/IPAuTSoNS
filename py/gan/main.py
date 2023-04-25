import stow
from engine import Engine
from animegan import AnimeGAN
import sys
import pymongo
import random
import string
import os
from os import *
from glob import glob

if __name__ == '__main__':
    job_id = sys.argv[1]
    useridparam = sys.argv[2]
    job = None
    folder = sys.argv[3]
    newfolder = sys.argv[4]
    ganmodel = sys.argv[5]
    folder = folder+"/*"
    All_files = glob(folder+'.png') + glob(folder+'.PNG') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.JPG') + glob(folder+'.JPEG') + glob(folder+'.tiff') + glob(folder+'.TIFF')


    
    client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
    db = client.ipautsons
    try:
        job = db.api_job.find_one({'job_id' : job_id})
    except NameError as error:
        job = None

    try:
        print("start")
        for x in range(len(All_files)):
            print(x)
            animegan = AnimeGAN(ganmodel)
            filename, extension = os.path.splitext(os.path.basename(All_files[x]))
            All_files[x].save(newfolder+"/"+filename+extension)
            newpath = newfolder+"/"+filename+extension
            engine = Engine(image_path=newpath, show=False,  custom_objects=[animegan])
            engine.run()
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
        print(error)
        if job != None and type(job) == dict:
            job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                            {"$set":
                                                                {'job_status' : 2
                                                                }
                                                            },upsert=True)





