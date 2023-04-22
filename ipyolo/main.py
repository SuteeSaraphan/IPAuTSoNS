from fastapi import FastAPI, File
from segmentation import get_yolov5, get_image_from_bytes
from starlette.responses import Response
import io
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

@app.post("/detect-to-json")
async def detect_garbage_return_json_result(file: bytes = File(...)):
    input_image = get_image_from_bytes(file)
    results = model(input_image)
    results = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
    class_counts = Counter(obj['name'] for obj in results)
    class_counts_dict = {name: count for name, count in class_counts.items()}
    if class_counts_dict == {}:
        input_image = get_image_from_bytes(file)
        results = model2(input_image)
        results = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
        class_counts = Counter(obj['name'] for obj in results)
        class_counts_dict = {name: count for name, count in class_counts.items()}
        if class_counts_dict == {}:
            input_image = get_image_from_bytes(file)
            results = model3(input_image)
            results = json.loads(results.pandas().xyxy[0].to_json(orient="records"))
            class_counts = Counter(obj['name'] for obj in results)
            class_counts_dict = {name: count for name, count in class_counts.items()}
    return class_counts_dict

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
async def detect_return_base64_img(folders = "",modelse = "yolov5n.pt",job_id = ""):
    folder = folders+"/*"
    
    All_files = glob(folder+'.png') + glob(folder+'.jpg') + glob(folder+'.jpeg') + glob(folder+'.tiff')

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
            img_base64.save(out_f)
        if job != None and type(job) == dict:
            job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                            {"$set":
                                                                {'job_status' : 1
                                                                }
                                                            },upsert=True)
    except:
      if job != None and type(job) == dict:
        job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                        {"$set":
                                                            {'job_status' : 2
                                                            }
                                                        },upsert=True)
        return dict(msg='Fail')

    return dict(msg='OK')