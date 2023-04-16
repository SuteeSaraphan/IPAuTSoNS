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
except:
  print("An exception occurred")
  if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 2
                                                        }
                                                    },upsert=True)

