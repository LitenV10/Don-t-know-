import os
import logging
import pickle
import codecs
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pyrogram.types import Message
from SmartEncoder.Database.db import myDB
from SmartEncoder.Plugins.list import *
from SmartEncoder.__main__ import *


async def on_task_complete(bot, message: Message):
  #del data[0]
 # if len(data) > 0:
   # await add_task(bot, data[0])
  myDB.lpop("DBQueue")
  queue_ = myDB.lindex("DBQueue", 0)
  if queue_ is None:
    return
  _queue = pickle.loads(codecs.decode(queue_.encode(), "base64"))
  value_ = myDB.llen("DBQueue")
  if value_ is None:
    return
  elif value_ > 0:
    await add_task(bot, _queue)

async def add_task(bot, message: Message):
  try:
    os.system('rm -rf /app/downloads/*')
    await SmartEncoder.Plugins.Labour.labour_encode(bot, message)
  except Exception as e:
    logger.info(e)
  value_ = myDB.llen("DBQueue")
  if value_ is None:
    return
  await on_task_complete(bot, message)
  
  
# async def _on_task_complete(bot, message: Message):
  # del rename_queue[0]
  # if len(rename_queue) > 0:
    # await add_rename(bot, rename_queue[0])

# async def add_rename(bot, message: Message):
  # try:
    # os.system('rm -rf /app/downloads/*')
    # await rename_pro(bot, message)
  # except Exception as e:
    # logger.info(e)  
  # await _on_task_complete(bot, message)
