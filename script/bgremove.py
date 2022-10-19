import sys
import glob
import numpy as np
import os
import psutil
import json
import datetime
import cv2

from rembg import remove
from glob import glob


def test():
    for x in range(len(All_files)):
        img = cv2.imread(All_files[x])
        output = remove(img)
        cv2.imwrite(All_files[x]+".png", output)
        os.remove(All_files[x])

def saveLog():
    # Data to be written
    dictionary = {
        "id": iduser,
        "job": command,
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
iduser = sys.argv[1] 
folder = sys.argv[2]
folder = folder+"/*"
All_files = glob(folder)

#saveLog()
test()
