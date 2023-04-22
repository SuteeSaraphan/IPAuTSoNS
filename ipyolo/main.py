from fastapi import FastAPI, File
from segmentation import get_yolov5, get_image_from_bytes
from starlette.responses import Response
import io
import string
import os
import random
from os import *
from PIL import Image
import base64
from collections import Counter
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import glob
from glob import glob
import pymongo



app = FastAPI(
    title="Ipautsons API YoloModel Preview",
    description="""Ipautsons API YoloModel Preview""",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return dict(msg='OK')

@app.post("/weight-checker")
async def detect_garbage_return_base64_img(file: bytes = File(...),modelse = "yolov5n.pt"):
    try:
        input_image = get_image_from_bytes(file)
        
        watermark = Image.open("watermark.png")
        width, height = input_image.size
        w_width, w_height = watermark.size
        x = (width - w_width) // 2
        y = (height - w_height) // 2
        input_image.paste(watermark, (x, y), watermark)
        model = get_yolov5(modelse)

        results = model(input_image)
        results.render()  # updates results.imgs with boxes and labels

        resultst = model(input_image)
        

        resultst = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
        class_counts = Counter(obj['name'] for obj in resultst)
        class_counts_dict = {name: count for name, count in class_counts.items()}
        


        for img in results.imgs:
            bytes_io = io.BytesIO()
            img_base64 = Image.fromarray(img)
            img_base64.save(bytes_io, format="jpeg")

    except NameError as error:
        return dict(msg=error) 

    return dict(msg="OK") 

@app.post("/detect-to-img")
async def detect_garbage_return_base64_img(file: bytes = File(...),modelse = "yolov5n.pt"):
    input_image = get_image_from_bytes(file)
    
    watermark = Image.open("watermark.png")
    width, height = input_image.size
    w_width, w_height = watermark.size
    x = (width - w_width) // 2
    y = (height - w_height) // 2
    input_image.paste(watermark, (x, y), watermark)
    model = get_yolov5(modelse)

    results = model(input_image)
    results.render()  # updates results.imgs with boxes and labels

    resultst = model(input_image)
    

    resultst = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
    class_counts = Counter(obj['name'] for obj in resultst)
    class_counts_dict = {name: count for name, count in class_counts.items()}
    


    for img in results.imgs:
        bytes_io = io.BytesIO()
        img_base64 = Image.fromarray(img)
        img_base64.save(bytes_io, format="jpeg")


    return Response(content=bytes_io.getvalue(), media_type="image/jpeg")

@app.post("/detect")
async def detect_return_base64_img(job_id = "",useridparam="",folders = "",modelse = "yolov5n.pt",newfolder = "",):
    folder = folders+"/*"
    
    All_files = glob(folder+'.png') + glob(folder+'.PNG') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.JPG') + glob(folder+'.JPEG') + glob(folder+'.tiff') + glob(folder+'.TIFF')  

    model = get_yolov5(modelse)
    client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
    db = client.ipautsons
    try:
        job = db.api_job.find_one({'job_id' : job_id})
    except NameError as error:
        job = None
    try:
        for x in range(len(All_files)):
            input_image = All_files[x]
            results = model(input_image)
            results.render()  # updates results.imgs with boxes and labels

            for img in results.imgs:
                bytes_io = io.BytesIO()
                img_base64 = Image.fromarray(img)
                img_base64.save(bytes_io, format="jpeg")
            out_f = All_files[x]
            filename, extension = os.path.splitext(os.path.basename(out_f))
            img_base64.save(newfolder+"/"+filename+extension)
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
      if job != None and type(job) == dict:
        job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                        {"$set":
                                                            {'job_status' : 2
                                                            }
                                                        },upsert=True)
        return dict(msg='Fail')

    return dict(msg='OK')