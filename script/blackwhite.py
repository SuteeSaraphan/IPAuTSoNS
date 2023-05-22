import sys
import json
import datetime
import pymongo
from glob import glob
from PIL import Image, ImageDraw, ImageFont

def BlackWhite():
    for x in range(len(All_files)):
        img = Image.open(All_files[x])
        imgGray = img.convert('L')
        imgGray.save(All_files[x])

def saveLog():
    # Data to be written
    dictionary = {
        "id": iduser,
        "job": "BlackWhite",
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
job = None
folder = sys.argv[2]
folder = folder+"/*"
All_files = glob(folder)
BlackWhite()
