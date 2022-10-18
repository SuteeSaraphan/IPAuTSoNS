import sys
import json
import datetime
from glob import glob
from PIL import Image, ImageDraw, ImageFont

def BlackWhite():
    img = Image.open(selected_img)
    imgGray = img.convert('L')
    width, height = imgGray.size

    draw = ImageDraw.Draw(imgGray)
    text = "sample IPAuTSoNS"

    font = ImageFont.truetype('arial.ttf', 100)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    # draw watermark in the bottom right corner
    draw.text((x, y), text,fill='cyan', font=font)  
    imgGray.save(selected_img, quality=10)

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
iduser = sys.argv[1] 
selected_img = sys.argv[2]
#folder = folder+"/*"
#All_files = glob(folder)

#saveLog()
BlackWhite()
