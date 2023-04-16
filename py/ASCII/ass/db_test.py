import pymongo

job_id = "test_02"
path = r"i6r6mvxzco\root\test02"
img_selected = "asdf.jpg"
num_img = "15"
job = None

client = pymongo.MongoClient("mongodb+srv://ipautsons:J0iZfrxW49cFOr4U@cluster0.lbe3op6.mongodb.net/?retryWrites=true&w=majority")
db = client.ipautsons
job = db.api_job.find_one({'id' : '1'})
print(job)
