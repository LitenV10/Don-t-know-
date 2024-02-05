# worker.py >
import os
import time
import asyncio 
from config import Config
#from SmartEncoder.__main__ import *

from smartencoder.Plugins.compress import en_co_de
from smartencoder.Tools.progress import *
from smartencoder.Plugins.list import *

async def labour_encode(bot, update):
  download_location = Config.DOWN_PATH + "/"
  sent_message = await bot.send_message(
    text="**DOWNLOADING**",
    chat_id=update.chat.id,
    reply_to_message_id=update.id
  )
  c_time = time.time()
  f_n = await bot.download_media(
    message=update,
    #myDB.lindex("DBQueue", 0),
    #file_name=download_location,
    progress=progress_for_pyrogram,
    progress_args=(
      bot,
      "**DOWNLOADING**",
      sent_message,
      c_time
    )
  )
  logger.info(f_n)
  await asyncio.sleep(1)
  if f_n is not None:
    await sent_message.edit_text("**TRYING TO ENCODE**")
  # if not .mkv or.mp4 or .webm
  if f_n.rsplit(".", 1)[-1].lower() not in ["mkv", "mp4", "webm", "avi"]:
    return await sent_message.edit_text("This format isnt allowed , please send only either **MKV** or **MP4** files.")
  # if in .mkv or .mp4 
  if "`" in f_n:
    _f_n = f_n.replace("`", "'")
    os.rename(f_n, _f_n)
  elif '"' in f_n:
    _f_n = f_n.replace("`", "'")
    os.rename(f_n, _f_n)
  else:
    _f_n = f_n
  o = await en_co_de(
    _f_n,
    sent_message
  )
  logger.info(o)
  # upload event 
  if o is None:
    await sent_message.edit_text("Either the current ffmpeg code didnt work on the file as it gave error or its an internal issue.\nContact the [dev](https://t.me/Bro_isDarkal)",
    disable_web_page_preview=True)
    os.remove(_f_n)
    return
  if o is not None:
    await sent_message.edit_text("UPLOADING")
    upload = await bot.send_document(
      chat_id=update.chat.id,
      document=o,
      force_document=True,
      #caption="©️ @Animes_Encoded",
      reply_to_message_id=update.id,
      progress=progress_for_pyrogram,
      progress_args=(bot, "UPLOADING", sent_message, c_time)
    )
    # remove uploaded file as it will free space
    os.remove(o)
    os.remove(_f_n)
    # in order to make bot organised 
    await sent_message.delete()
