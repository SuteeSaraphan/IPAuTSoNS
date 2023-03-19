import sys
import glob
import numpy as np
import os
import json
import datetime
import pymongo

from glob import glob
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont


def ASCII():
    for x in range(len(All_files)):
        print("haha")
        print(x)
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
        newImg.save(out_f)

def saveLog():
    # Data to be written
    dictionary = {
        "id": iduser,
        "job": "ASCII",
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

print("haha")
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
except:
  print("An exception asd")
  if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 2
                                                        }
                                                    },upsert=True)


