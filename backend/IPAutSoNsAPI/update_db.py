import pymongo

job_id = "test_02"
path = r"i6r6mvxzco\root\test02"
img_selected = "asdf.jpg"
num_img = "15"
job = None

client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons
try:
    job = db.api_job.find_one({'job_id' : job_id})
except NameError as error:
    job = None
    print(error)

if job != None and type(job) == dict:
    job = db.api_job.find_one_and_update({'job_id' : job_id},
                                                    {"$set":
                                                        {'job_status' : 1,
                                                        'path' :path,
                                                        'num_img' : num_img ,
                                                        'img_selected' : img_selected
                                                        }
                                                    },upsert=True)

