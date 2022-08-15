import pymongo
from pymongo import MongoClient
import time


cluster = pymongo.MongoClient("mongodb+srv://peach:0880353429@cluster0.j9edmy6.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]
collectuin = db["percen"]

#post = {"_id":0,"user":77,"percen":0,"workcount":0}
#collectuin.insert_one(post)
x = 0
for i in range(10):
	time.sleep(1)
	x=x+10
	print(x)
	up = collectuin.update_one({"_id":0}, {"$set":{"percen":x,"workcount":x}})