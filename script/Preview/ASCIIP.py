import sys
import glob
import numpy as np
import os
import json
import datetime

from glob import glob
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont
from keras.preprocessing import image

def ASCII():
    SC = 0.1    # pixel sampling rate in width
    GCF= 2 
    color1='black'
    color2='blue'
    bgcolor='white'
    img = Image.open(selected_img)
    #img = ("image_name2.jpg", quality=25)
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
    width, height = newImg.size

    draw = ImageDraw.Draw(newImg)
    text = "sample IPAuTSoNS"

    font = ImageFont.truetype('arial.ttf', 100)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    # draw watermark in the bottom right corner
    draw.text((x, y), text,fill='cyan', font=font)                     
    out_f = selected_img
    
    newImg.save(out_f, quality=10)

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
iduser = sys.argv[1] 
selected_img = sys.argv[2]


#saveLog()
ASCII()
