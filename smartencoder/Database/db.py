# redis db 
import redis
from config import Config, REDIS_PORT

myDB = redis.Redis(
  host=Config.REDIS_HOST,
  port=REDIS_PORT,
  password=Config.REDIS_PASS,
  decode_responses=True
)
import pymongo 
import os
DB_NAME = os.environ.get("DB_NAME","cluster0")
DB_URL = os.environ.get("DB_URL","mongodb+srv://power:power@cluster0.ncgr0eh.mongodb.net/?retryWrites=true&w=majority")
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]
def total_user():
      user = dbcol.count_documents({})
      return user
      
#insert bot Data 
def botdata(chat_id):
   bot_id = int(chat_id)
   try:
      bot_data = {"id":bot_id}
      dbcol.insert_one(bot_data)
   except:
      pass
def find(chat_id):
    id =  {"id":chat_id}
# def new_user(id):
    # return dict(id=id)
# async def add_user(id):
        # user = dbcol.new_user(id)
        # await dbcol.insert_one(user)
async def is_user_exist(id):
        user = dbcol.find_one({'id':int(id)})
        return True if user else False
def getid():
    values = []
    for key  in dbcol.find():
         id = key["id"]
         values.append((id)) 
    return values
async def insert(chat_id):
            user_id = int(chat_id)
            user_det = {"id":user_id}
            dbcol.insert_one(user_det)
async def set_caption(id, caption):
        dbcol.update_one({'id': int(id)}, {'$set': {'caption': caption}})
async def get_caption(id):
        user = dbcol.find_one({'id': int(id)})
        return user.get('caption', None)
async def set_thumbnail(id, file_id):
        dbcol.update_one({'id': int(id)}, {'$set': {'file_id': file_id}})
async def get_thumbnail(id):
        user = dbcol.find_one({'id': int(id)})
        return user.get('file_id', None)
def delete(id):
    dbcol.delete_one(id)
  
