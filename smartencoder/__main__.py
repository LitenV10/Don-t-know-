# i am using redis db. Its quite handy and easy. i used lists for queue. and redis can only store bytes, str, int or float. so i used codecs to encode list[0] in str then stored in db. when using the stored str, i equated it later decoded it back in its original type using 'codecs' module.
from . import TGBot
import logging
import asyncio 
import time
import string
import pickle # to dumps/loads 
import codecs # to encode/decode basically
import requests
import motor.motor_asyncio
#import json cuz i dont nedd this fucking module
#import urllib3 as url ahh
from pyrogram.file_id import FileId
import os
import gdown 
from umongo import Instance, Document, fields
from aria2p import API as ariaAPI, Client as ariaClient
#from ethon.uploader import weburl, ytdl
import re
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
import shutil
import psutil
import math
from PyPDF2 import PdfMerger
import subprocess
import random
from PIL import Image
import yt_dlp as yt
from yt_dlp.utils import DownloadError
from pytube import YouTube
from pytube import Playlist
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import threading
from pyrogram.errors import MessageNotModified, FloodWait, UserNotParticipant
from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from smartencoder.Plugins.renamer import *
from datetime import datetime as dt
#from smartencoder.Plugins.compress import *
# database 
from smartencoder.Database.db import is_user_exist, insert, myDB, get_caption, set_caption, get_thumbnail, set_thumbnail, delete,getid
import smartencoder.Plugins.Labour
from smartencoder.Plugins.Queue import *
from smartencoder.Plugins.list import *
from smartencoder.Plugins.ffmg import OpenSettings, trimmer, MergeVideo, generate_screen_shots, cult_small_video, take_screen_shot, fix_thumb, MakeButtons, delete_all, extr_files, get_files
#from smartencoder.Plugins.ffmg import *
from smartencoder.Tools.eval import *
from smartencoder.Addons.download import d_l
from smartencoder.Addons.executor import bash_exec
from smartencoder.Plugins.cb import *
from smartencoder.Addons.list_files import l_s
from smartencoder.translation import Translation
from smartencoder.Tools.progress import *
from config import Config
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from pyrogram import enums
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pathlib import Path
mode_for_custom = []
folder = []
batch = []
QueueDB = {}
ReplyDB = {}
FormtDB = {}
tmkyt = []
tmkyt.append("off")
ADMIN = int(os.environ.get("ADMIN", "2067727305"))
uptime = dt.now()
mode_for_custom.append("off")
if not os.path.isdir(Config.DOWN_PATH):
    os.makedirs(Config.DOWN_PATH)
#########################################
aria2 = ariaAPI(ariaClient(host="http://localhost", port=6800, secret=""))
def aria2c_init():
    try:
        logger.info("Initializing Aria2c")
        link = "https://linuxmint.com/torrents/lmde-5-cinnamon-64bit.iso.torrent"
        dire = Config.DOWN_PATH.rstrip("/")
        aria2.add_uris([link], {'dir': dire})
        time.sleep(3)
        downloads = aria2.get_downloads()
        time.sleep(15)
        aria2.remove(downloads, force=True, files=True, clean=True)
    except Exception as e:
        logger.info(f"Aria2c initializing error: {e}")
threading.Thread(target=aria2c_init).start()
time.sleep(1.5)
aria2_options = aria2.client.get_global_option()
del aria2_options['dir']
#########################################
async def resume_task():
    if myDB.llen("DBQueue") > 0:
        queue_ = myDB.lindex("DBQueue", 0)
        if queue_ is not None:
            _queue = pickle.loads(codecs.decode(queue_.encode(), "base64"))
            await add_task(TGBot, _queue)
        else:
            print("Error: Queue is None.")
    else:
        print("Error: Queue length is 0.")
        
async def start_bot():
  await TGBot.start()
  await resume_task()
  await idle()


#if __name__ == "__main__":
    #loop.run_untill_complete(start_bot())
#rename_task.insert(0, "on")
if __name__ == "__main__":
  @TGBot.on_message(filters.incoming & (filters.video | filters.audio | filters.document))
  async def wah_1_man(bot, message: Message):
    if mode_for_custom[0] == "off":
      if message.from_user.id not in Config.AUTH_USERS:
        return
      if rename_task[0] == "off":
        a = message
        #data.append(a)
        # using a as message is easy
        pickled = codecs.encode(pickle.dumps(a), "base64").decode()
        myDB.rpush("DBQueue", pickled)
        query = await message.reply_text(f'Aᴅᴅᴇᴅ ᴛʜɪs ғɪʟᴇ ɪɴ #{myDB.llen("DBQueue")} ɪɴ ǫᴜᴇᴜᴇ.\nCᴏᴍᴘʀᴇss ᴡɪʟʟ sᴛᴀʀᴛ sᴏᴏɴ.', quote=True)
        if myDB.llen("DBQueue") == 1:
        #if len(data) == 1:
          await query.delete()
          await add_task(bot, message)
      elif rename_task[0] == "pdfmrg":
          b = message
          pdfiles.append(b)
          if tmkyt[0] == "on":
             await addpdf(bot, message)
          else:
             ms = await message.reply_text(f"Added it \nThere are {len(pdfiles)} PDF to merge💥 Send more to add more 🔥\nsend /lastpdf when you are done! 😃")
      elif rename_task[0] == "audiomrg":
          c = message
          audiofiles.append(c)
          if tmkyt[0] == "aud":
             await addaudio(bot, message)
          else:
             ms = await message.reply_text(f"Added it \nThere are {len(audiofiles)} Audio to merge💥 Send more to add more 🔥\nsend /lastaud when you are done! 😃")
      elif rename_task[0] == "merge":
          media = message.video or message.document
          if media.file_name is None:
              await message.reply_text("File Name Not Found!")
              return
          if media.file_name.rsplit(".", 1)[-1].lower() not in ["mp4", "mkv", "webm"]:
               await message.reply_text("This Video Format not Allowed!\nOnly send MP4 or MKV or WEBM.", quote=True)
               return
          if QueueDB.get(message.from_user.id, None) is None:
               FormtDB.update({message.from_user.id: media.file_name.rsplit(".", 1)[-1].lower()})
          if (FormtDB.get(message.from_user.id, None) is not None) and (media.file_name.rsplit(".", 1)[-1].lower() != FormtDB.get(message.from_user.id)):
              await message.reply_text(f"First you sent a {FormtDB.get(message.from_user.id).upper()} video so now send only that type of video.", quote=True)
              return
          input_ = f"{Config.DOWN_PATH}/{message.from_user.id}/input.txt"
          if os.path.exists(input_):
               await message.reply_text("Sorry Unkil,\nAlready One in Progress!\nDon't Spam.")
               return
          mm = 2
        #  isInGap, sleepTime = await CheckTimeGap(message.from_user.id)
          if mm == 9:
               await message.reply_text(f"Sorry Sir,\nNo Flooding Allowed!\nSend Video After")
          #`{str(sleepTime)}s` !!", quote=True)
          else:
               editable = await message.reply_text("Please Wait ...", quote=True)
               MessageText = "Okay,\nNow Send Me Next Video or Press **Merge Now** Button!"
          if QueueDB.get(message.from_user.id, None) is None:
            QueueDB.update({message.from_user.id: []})
          if (len(QueueDB.get(message.from_user.id)) >= 0) and (len(QueueDB.get(message.from_user.id)) <= Config.MAX_VIDEOS):
            QueueDB.get(message.from_user.id).append(message.id)
            if ReplyDB.get(message.from_user.id, None) is not None:
                await bot.delete_messages(chat_id=message.chat.id, message_ids=ReplyDB.get(message.from_user.id))
            if FormtDB.get(message.from_user.id, None) is None:
                FormtDB.update({message.from_user.id: media.file_name.rsplit(".", 1)[-1].lower()})
            if len(QueueDB.get(message.from_user.id)) == Config.MAX_VIDEOS:
                MessageText = "Okay Unkil, Now Just Press **Merge Now** Button 15 videos!"
            markup = await MakeButtons(bot, message, QueueDB)
            await editable.edit(text="Your Video Added to Queue!")
            reply_ = await message.reply_text(
                text=MessageText,
                reply_markup=InlineKeyboardMarkup(markup),
                quote=True
            )
            ReplyDB.update({message.from_user.id: reply_.id})
          elif len(QueueDB.get(message.from_user.id)) > Config.MAX_VIDEOS:
            markup = await MakeButtons(bot, message, QueueDB)
            await editable.edit(
                text=f"Sorry Unkil,\nMax {str(Config.MAX_VIDEOS)} Videos Allowed to Merge Together!\nPress **Merge Now** Button Now!",
                reply_markup=InlineKeyboardMarkup(markup)
            )
      else:
        if message.from_user.id not in Config.AUTH_USERS:
          return 
        chat_id = message.chat.id
        message_id = message.id
        media = await bot.get_messages(chat_id=chat_id, message_ids=message_id)
        #media = await bot.get_messages(message.chat.id)
        file = media.document or media.video or media.audio 
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size)
        await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {filesize}\n**Dc ID** :- {dcid}""",reply_to_message_id = message_id,reply_markup = InlineKeyboardMarkup(
          [[ InlineKeyboardButton("📝 Rename",callback_data = "rename"),
          InlineKeyboardButton("✖️ Cancel",callback_data = "msgdel")  ]]))
        # query = await message.reply_text("Aᴅᴅᴇᴅ ᴛʜɪs ғɪʟᴇ ᴛᴏ ʀᴇɴᴀᴍᴇ ɪɴ ǫᴜᴇᴜᴇ.", quote=True)
        # rename_queue.append(message)
        # if len(rename_queue) == 1:
          # await query.delete()
          # await add_rename(bot, message)

  @TGBot.on_message(filters.incoming & filters.command("rename_mode", prefixes=["/", "."]))
  async def help_eval_message(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    OUT = "Rᴇɴᴀᴍᴇ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ."
    await message.reply_text(OUT, quote=True)
    rename_task.insert(0, "on")
    
  @TGBot.on_message(filters.incoming & filters.command("merge_mode", prefixes=["/", "."]))
  async def help_eval_message(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    OUT = "Merge ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ."
    await message.reply_text(OUT, quote=True)
    rename_task.insert(0, "merge")
    
  @TGBot.on_message(filters.incoming & filters.command("pdf_mode", prefixes=["/", "."]))
  async def help_eval_message(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    OUT = "PDF Merge ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ."
    await message.reply_text(OUT, quote=True)
    rename_task.insert(0, "pdfmrg")
    
  @TGBot.on_message(filters.incoming & filters.command("Audio_mode", prefixes=["/", "."]))
  async def help_eval_message(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    OUT = "Audio Merge ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ."
    await message.reply_text(OUT, quote=True)
    rename_task.insert(0, "audiomrg")
    
  @TGBot.on_message(filters.incoming & filters.command("eval", prefixes=["/", "."]))
  async def help_eval_message(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    await eval_handler(bot, message)
  
  @TGBot.on_message(filters.command("dl", prefixes=["/", "."]))
  async def start_cmd_handler(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
      return
    await d_l(bot, update)

  @TGBot.on_message(filters.command("ul", prefixes=["/", "."]))
  async def u_l(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    c_time = time.time()
    input_message = message.text.split(" ", maxsplit=1)[1]
    path = Path(input_message)
 # start = datetime.now()
    if not os.path.exists(path):
      await message.reply_text(f"No such file or directory as `{path}` found", quote=True)
      return
    boa = await message.reply_text("**UPLOADING**", quote=True)
    await bot.send_document(
      chat_id=message.chat.id,
      document=path,
      force_document=True,
      #caption="©️ @Animes_Encoded",
      reply_to_message_id=message.id,
      progress=progress_for_pyrogram,
      progress_args=(bot, "UPLOADING", boa, c_time)
    )
    await boa.delete()
  
# bash
  @TGBot.on_message(filters.command("bash", prefixes=["/", "."]))
  async def start_cmd_handler(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    await bash_exec(bot, message)

# ls
  @TGBot.on_message(filters.incoming & filters.command("ls", prefixes=["/", "."]))
  async def lost_files(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    await l_s(bot, message)

# disable normal mode
  @TGBot.on_message(filters.command("manual_mode", prefixes=["/", "."]))
  async def hehe(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return 
    await message.reply_text("ɪ ᴡɪʟʟ ɴᴏᴡ ᴡᴏɴᴛ ʀᴇsᴘᴏɴᴅ ᴛᴏ ᴀɴy ғɪʟᴇ! ʀᴇᴘʟy ᴍᴇ ᴡɪᴛʜ /dl ᴀɴᴅ /ul", quote=True)
    mode_for_custom.insert(0, "on")
  
# able normal mode
  @TGBot.on_message(filters.command("normal_mode", prefixes=["/", "."]))
  async def hehe(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return 
    await message.reply_text("ɪ ᴡɪʟʟ ɴᴏᴡ ʀᴇsᴘᴏɴᴅ ᴛᴏ ᴀɴy sᴇɴᴛ ғɪʟᴇ", quote=True)
    mode_for_custom.insert(0, "off")
    rename_task.insert(0, "off")
#########################################
  @TGBot.on_message(filters.command("start", prefixes=["/", "."]))
  async def start_cmd_handler(bot, message):
        if not await is_user_exist(message.from_user.id):
            await insert(message.from_user.id)
        await message.reply_text(
            text=Translation.START_TEXT,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ʜᴇʟᴘ", callback_data="hilp")
                    ]
                ]
            ),
            parse_mode=enums.ParseMode.MARKDOWN
        )
#########################################
  def drive_folder_download(url):
        output = gdown.download_folder(url, quiet=True)
        return output
  def edit_msg(client, message, to_edit):
    try:
        client.loop.create_task(message.edit(to_edit))
    except FloodWait as e:
        client.loop.create_task(asyncio.sleep(e.value))
    except MessageNotModified:
        pass
    except TypeError:
        pass
#########################################
  def get_size(size):
        units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
        size = float(size)
        i = 0
        while size >= 1024.0 and i < len(units):
            i += 1
            size /= 1024.0
        return "%.2f %s" % (size, units[i])
  def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'B'
  def download_progress_hook(d, message, client):
    if d['status'] == 'downloading':
        current = d.get("_downloaded_bytes_str") or humanbytes(int(d.get("downloaded_bytes", 1)))
        tot = d.get("total_bytes") or d.get("total_bytes_estimate")
        total = humanbytes(tot)
        file_name = d.get("filename")
        downloaded_bytes = d.get("downloaded_bytes")   
        eta = d.get('_eta_str', "N/A")
        progress = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        to_edit = f"📥 <b>Downloading!</b>\n\n<b>Name :</b> <code>{file_name}</code>\n<b>Size :</b> <code>{total}</code>\n<b>Speed :</b> <code>{speed}</code>\n<b>ETA :</b> <code>{eta}</code>\n\n<b>Downloaded: </b> <code>{current}</code> from <code>{total}</code> \n<b>Percentage: </b> <code>{progress}</code>"
        threading.Thread(target=edit_msg, args=(client, message, to_edit)).start()
#########################################
  async def upload_folder(bot, boa, message):
        index = len(folder)
        for i in range(int(index)):
            try:
                file = folder[int(i)]
                timey = time.time()
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=file,
                    force_document=True,
                    caption=f"©️ @Animes_Encoded #{int(i)}",
                    reply_to_message_id=message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "UPLOADING.", boa, timey)
                )
                folder.remove(file)
                await boa.delete()
                os.remove(file)
            except Exception as e:
                print(e)
  async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)
  ss = os.environ.get("STRING", "")
  if ss is not None:
      acc = Client(session_string=ss, api_id=Config.API_ID, api_hash=Config.API_HASH)
      acc.start()
  else:
      acc = None
      #session_name instead of session_string because pyrogram 1.4.16
  frgb = ""
  if frgb is not None:
      acfr = Client(session_string=frgb, api_id=Config.API_ID, api_hash=Config.API_HASH)
      acfr.start()
  else:
      acfr = None
  async def Mdata01(download_directory):
          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
          return width, height, duration
#########################################
  async def run_batch(userbot, client, sender, link, _range, message):
      for i in range(_range):
          timer = 60
          if i < 25:
              timer = 5
          if i < 50 and i > 25:
              timer = 10
          if i < 100 and i > 50:
              timer = 15
          if not 't.me/c/' in link:
              if i < 25:
                  timer = 2
              else:
                  timer = 3
          try: 
              if not sender in batch:
                  await client.send_message(sender, "Batch completed.")
                  break
          except Exception as e:
              print(e)
              await client.send_message(sender, "Batch completed.")
              break
          try:
              await get_bulk_msg(userbot, client, sender, link, i, message) 
          except FloodWait as fw:
              if int(fw.x) > 299:
                  await client.send_message(sender, "Cancelling batch since you have floodwait more than 5 minutes.")
                  break
              await asyncio.sleep(fw.x + 5)
              await get_bulk_msg(userbot, client, sender, link, i, message)
          protection = await client.send_message(sender, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
          await asyncio.sleep(timer)
          await protection.delete()
#########################################
  async def get_bulk_msg(userbot, client, sender, msg_link, i, message):
      if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
      datas = msg_link.split("/")
      msgid = int(datas[-1]) + int(i)
      if "https://t.me/c/" in msg_link:
          chatid = int("-100" + datas[-2])
          try: handle_private(client,message,chatid,msgid)
          except Exception as e: await client.send_message(sender, f"**Error** : __{e}__", reply_to_message_id=message.id)
      else:
          username = datas[-2]
          msg  = await client.get_messages(username,msgid)
          try: await client.copy_message(message.chat.id, msg.chat.id, msg.id,reply_to_message_id=message.id) #msg.id
          except:
              if acc is None:
                 await client.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
                 return
              try: handle_private(client,message,username,msgid)
              except Exception as e: await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
      
#########################################
  async def handle_private(bot,message,chatid,msgid):
    msg  = acc.get_messages(chatid,msgid)
    if "text" in str(msg):
        await bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return
    smsg = await bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
    ctimey = time.time()
    file = acc.download_media(msg, progress=progress_for_pyrogram, progress_args=(bot, "DOWNLOADING", smsg, ctimey))
    timey = time.time()
    if "Document" in str(msg):
        try:
           thumb = acc.download_media(msg.document.thumbs[0].file_id)
        except: thumb = None
        await bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress_for_pyrogram, progress_args=(bot, "UPLOADING", smsg, timey))
        if thumb != None: os.remove(thumb)
    elif "Video" in str(msg):
        try: 
           thumb = acc.download_media(msg.video.thumbs[0].file_id)
        except: thumb = None
        await bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress_for_pyrogram, progress_args=(bot, "UPLOADING", smsg, timey))
        if thumb != None: os.remove(thumb)
    elif "Animation" in str(msg):
        await bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
    elif "Sticker" in str(msg):
        await bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)
    elif "Voice" in str(msg):
        await bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress_for_pyrogram, progress_args=(bot, "UPLOADING", smsg, timey))
    elif "Audio" in str(msg):
        try:
           thumb = acc.download_media(msg.audio.thumbs[0].file_id)
        except: thumb = None
        await bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress_for_pyrogram, progress_args=(bot, "UPLOADING", smsg, timey))
        if thumb != None: os.remove(thumb)
    elif "Photo" in str(msg):
        await bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)
    os.remove(file)
    await bot.delete_messages(message.chat.id,[smsg.id]) #smsg.id
#########################################
  url_pattern = r'(https?://[^\s]+)'
  @TGBot.on_message(filters.incoming & filters.private & filters.regex(url_pattern))
  async def urlup(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        link = message.text
        boa = await message.reply_text("**DOWNLOADING**")
        file = None
        if 'drive.google.com' and 'folder' in link:
            try:
                output = drive_folder_download(link)
            except Exception as e:
                print(e)
                return await boa.edit(f'error {e}')
            if output is None:
                return await boa.edit("Could not Download!")
            index = len(output)
            for i in range(int(index)):
                folder.append((output)[i])
            await boa.edit("**UPLOADING**")
            await upload_folder(bot, boa, message)
        elif 'drive.google.com' and 'folders' in link:
            try:
                output = drive_folder_download(link)
            except Exception as e:
                print(e)
                return await boa.edit(f'error {e}')
            if output is None:
                return await boa.edit("Could not Download!")
            index = len(output)
            for i in range(int(index)):
                folder.append((output)[i])
            await boa.edit("**UPLOADING**")
            await upload_folder(bot, boa, message)
        elif 'https://drive.google.com/file/' in link:
            id = (link.split("/"))[5]
            _link = f'https://drive.google.com/uc?id={id}'
            try:
                file = gdown.download(_link, quiet=True)
            except Exception as e:
                print(e)
                return await boa.edit(f'error {e}')
            folder.append(file)
            await boa.edit("**UPLOADING**")
            await upload_folder(bot, boa, message)
        elif 'https://drive.google.com/uc?id=' in link:
            try:
                file = gdown.download(link, quiet=True)
            except Exception as e:
                print(e)
                return await boa.edit(f'error {e}')
            folder.append(file)
            await boa.edit("UPLOADING...")
            await upload_folder(bot, boa, message)
        elif 'drive.google.com' and 'id=' in link:
            try:
                link_ = f'https://drive.google.com/uc?id={(link.split("id="))[1]}'
                file = gdown.download(link_, quiet=True)
            except Exception as e:
                print(e)
                return await boa.edit(f'error {e}')
            folder.append(file)
            await boa.edit("UPLOADING...")
            await upload_folder(bot, boa, message)
        elif 't.me' in link:
            await boa.delete()
            if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
               if acc is None:
                   await bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
                   return
               try:
                   try: acc.join_chat(message.text)
                   except Exception as e: 
                        await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
                        return
                   await bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.id)
               except UserAlreadyParticipant:
                   await bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.id)
               except InviteHashExpired:
                   await bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.id)
            elif "https://t.me/" in message.text:
                datas = message.text.split("/")
                msgid = int(datas[-1].split("?")[0])
                # private
                if "https://t.me/c/" in message.text:
                     chatid = int("-100" + datas[-2])
                     if acc is None:
                          await bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
                          return
                     try: handle_private(bot,message,chatid,msgid)
                     except Exception as e: await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
                else:
                    username = datas[-2]
                    msg  = await bot.get_messages(username,msgid)
                    try: await bot.copy_message(message.chat.id, msg.chat.id, msg.id,reply_to_message_id=message.id) #msg.id
                    except:
                        if acc is None:
                           await bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
                           return
                        try: handle_private(bot,message,username,msgid)
                        except Exception as e: await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
        elif "tg://openmessage?user_id=" in link:
            await boa.delete()
            msg = re.match(
                r"tg:\/\/openmessage\?user_id=([0-9]+)&message_id=([0-9]+)", link
            )
            chat = msg[1]
            msg_id = int(msg[2])
            if chat.isdigit():
                chat = int(chat)
            try: handle_private(bot,message,chat,msg_id)
            except Exception as e: await bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
        elif 'terabox' in link:
            path = f"{Config.DOWN_PATH}/{message.from_user.id}"
            if not os.path.isdir(path):
              os.makedirs(path)
            args = {'dir': path, 'max-upload-limit': '1K', 'netrc-path': '/usr/src/app/.netrc'}
            download = aria2.add_uris([link], args)
            if download.error_message:
                error = str(download.error_message).replace('<', ' ').replace('>', ' ')
                logger.info(f"Download Error: {error}")
                return await boa.edit(f'{error}')
            gid = download.gid
            t_file = aria2.get_download(gid)
            complete = False
            while not complete:
                complete = t_file.is_complete
                if not complete and not t_file.error_message:
                    if t_file.has_failed:
                        return await boa.edit("Download cancelled!\n\nstatus- **FAILED**")
                    percentage = int(t_file.progress)
                    downloaded = percentage * int(t_file.total_length) / 100
                    current = humanbytes(downloaded)
                    total = t_file.total_length_string()
                    file_name = t_file.name
                    eta = t_file.eta_string()
                    progress = t_file.progress_string()
                    speed = t_file.download_speed_string()
                    leechers = t_file.connections
                    seeders = t_file.num_seeders
                    prog_str = "[{0}] |".format(
                    "".join(
                        "█"
                        for i in range(math.floor(percentage / 10))
                    ))
                    to_edit = f"📥 <b>Downloading!</b>\n{prog_str}\n\n<b>Name :</b> <code>{file_name}</code>\n<b>Size :</b> <code>{total}</code>\n<b>Leechers :</b> <code>{leechers}</code>\n<b>Seeders :</b> <code>{seeders}</code>\n<b>Speed :</b> <code>{speed}</code>\n<b>ETA :</b> <code>{eta}</code>\n\n<b>Downloaded: </b> <code>{current}</code> from <code>{total}</code> \n<b>Percentage: </b> <code>{progress}</code>"
                    threading.Thread(target=edit_msg, args=(bot, boa, to_edit)).start()
                else:
                    if complete:
                        for file in os.listdir(path):
                              if file.endswith((".mp4", ".mkv", ".webm")):
                                  #width, height, duration = await Mdata01(file)
                                  duration = 0
                                  metadata = extractMetadata(createParser(file))
                                  if metadata.has("duration"):
                                       duration = metadata.get("duration").seconds
                                  try:
                                     ph_path_ = await take_screen_shot(file,os.path.dirname(os.path.abspath(file)), random.randint(0, duration - 1))
                                     width, height, ph_path = await fix_thumb(ph_path_)
                                  except Exception as e:
                                     ph_path = None
                                     print(e)
                                  timey = time.time()
              #                    await boa.reply_video(
                                  await acfr.send_video(
                                      f"{file}",
                                      supports_streaming=True, 
                                      duration=duration,
                                      width=width,
                                      height=height,
                                      thumb=ph_path,
                                      progress=progress_for_pyrogram,
                                      progress_args=(bot, "UPLOADING", boa, timey),
                                      caption="The content you requested has been successfully downloaded!",
                                      reply_markup=InlineKeyboardMarkup(
                                             [
                                                 [
                                                    InlineKeyboardButton("• Owner •", url="https://t.me/dhruvprajapati2"),
                                                 ],
                                             ],
                                      ),
                                  )
                                  os.remove(f"{file}")
                                  break
                              else:
                                  continue
                        await boa.delete()
                        shutil.rmtree(path)
        elif 'youtu.be' or 'youtube' in link and not 'playlist' in link:
            global ythd
            global yt240p
            global yt360p
            global yt480p
            global yt
            global thumb
            global ytaudio
            yt = YouTube(link)
            thumb = yt.thumbnail_url
            ythd = yt.streams.get_highest_resolution()
            yt480p = yt.streams.get_by_resolution(resolution ='480p')
            yt240p = yt.streams.get_by_resolution(resolution ='240p')
            yt360p = yt.streams.get_by_resolution(resolution ='360p')
            ytaudio = yt.streams.filter(only_audio=True).first()
            audio_size = f"{int(format_bytes(ytaudio.filesize)[0]):.2f}{format_bytes(ytaudio.filesize)[1]}"
            hd = f"{int(format_bytes(ythd.filesize)[0]):.2f}{format_bytes(ythd.filesize)[1]}"
            yt2m = f"{int(format_bytes(yt240p.filesize)[0]):.2f}{format_bytes(yt240p.filesize)[1]}"
            yt3m = f"{int(format_bytes(yt360p.filesize)[0]):.2f}{format_bytes(yt360p.filesize)[1]}"
            yt4m = f"{int(format_bytes(yt480p.filesize)[0]):.2f}{format_bytes(yt480p.filesize)[1]}"
            result_buttons2 = InlineKeyboardMarkup(
              [[
                  InlineKeyboardButton('🎬 240P ' +' ⭕️ '+ yt2m, callback_data='240p'),
                  InlineKeyboardButton('🎬 360p ' + '⭕️ ' +  yt3m, callback_data='360p')
              ],[
                  InlineKeyboardButton('🎬 480P ' +' ⭕️ '+ yt4m, callback_data='480p'),
                  InlineKeyboardButton('🎬 720p [•Max] ' + '⭕️ ' + hd, callback_data='high')
              ],[
                  InlineKeyboardButton('🎧 AUDIO '+  '⭕️ ' +  audio_size , callback_data='audio')
              ],[
                  InlineKeyboardButton('🖼THUMBNAIL🖼', callback_data='thumbnail')
              ]]
            )
            await message.reply_photo(
                    photo=thumb,
                    caption="🎬 TITLE : "+ yt.title +  "\n\n📤 UPLOADED : " + yt.author  + "\n\n📢 CHANNEL LINK " + f'https://www.youtube.com/channel/{yt.channel_id}',
                    reply_markup=result_buttons2,
                    quote=True,
            
            )
        elif 'playlist' in link:
            pyt = Playlist(link)
            await boa.delete()
            for video in pyt.videos:
                  try:
                      phd = video.streams.get_by_resolution(resolution ='360p')
                      wide = phd.download()
                  except:
                        phd = video.streams.get_highest_resolution()
                        wide = phd.download()
                  duration = 0
                  metadata = extractMetadata(createParser(wide))
                  if metadata.has("duration"):
                         duration = metadata.get("duration").seconds
                  #width, height, duration = await Mdata01(wide)
                  try:
                     ph_path_ = await take_screen_shot(wide, os.path.dirname(os.path.abspath(wide)), random.randint(0, duration - 1))
                     width, height, ph_path = await fix_thumb(ph_path_)
                  except Exception as e:
                       ph_path = None
                       print(e)
                  timey = time.time()
                  sent = await bot.send_message(
                    text="**DOWNLOADING**",
                    chat_id=message.chat.id,
                    reply_to_message_id=message.id
                  )
                  await acfr.send_video(
                            chat_id = message.chat.id, 
                            supports_streaming=True,
                            duration=duration,
                            width=width,
                            height=height,
                            thumb=ph_path,
                            caption=(f"⭕️ PLAYLIST : "+ pyt.title + "\n📥 DOWNLOADED " + "\n✅ JOIN @HKBOTZ" ),
                            video = wide,
                            progress=progress_for_pyrogram,
                            progress_args=(bot, "UPLOADING", sent, timey)
                  )
                  os.remove(wide)
                  await sent.delete()
                  try:
                     os.remove(ph_path)
                  except:
                     pass
        else:
            ydl_opts = {
                #'format': 'bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480]',
                "format": "best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
                "ignoreerrors": True,
                "usenetrc": True,
                "cookiefile": "cookies.txt",
                "allow_multiple_video_streams": True,
                "allow_multiple_audio_streams": True,
                "noprogress": True,
                "allow_playlist_files": True,
                "overwrites": True,
                # "outtmpl": "%(id)s.mp4",
                "logtostderr": False,
                #"quiet": True,
                # outtmpl: '%(title)s.%(ext)s',
                "progress_hooks": [lambda d: download_progress_hook(d, boa, bot)]
            }
            with yt.YoutubeDL(ydl_opts) as ydl:
                try:
                   ytdl_data = ydl.extract_info(link, download=False)
                   await run_async(ydl.download, [link])
                except DownloadError as d:
                   await boa.edit(f"Sorry, an error {d} occurred")
                   return
            for file in os.listdir('.'):
                if file.endswith((".3gp", ".avi", ".flv", ".mp4", ".mkv", ".mov", ".mpeg", ".mpg", ".webm")):
                    #width, height, duration = await Mdata01(file)
                    duration = 0
                    metadata = extractMetadata(createParser(file))
                    if metadata.has("duration"):
                         duration = metadata.get("duration").seconds
                    try:
                       ph_path_ = await take_screen_shot(file,os.path.dirname(os.path.abspath(file)), random.randint(0, duration - 1))
                       width, height, ph_path = await fix_thumb(ph_path_)
                    except Exception as e:
                       ph_path = None
                       print(e)
                    timey = time.time()
#                    await boa.reply_video(
                    await acfr.send_video(
                        f"{file}",
                        supports_streaming=True, 
                        duration=duration,
                        width=width,
                        height=height,
                        thumb=ph_path,
                        progress=progress_for_pyrogram,
                        progress_args=(bot, "UPLOADING", boa, timey),
                        caption="The content you requested has been successfully downloaded!",
                        reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                      InlineKeyboardButton("• Owner •", url="https://t.me/dhruvprajapati2"),
                                   ],
                               ],
                        ),
                    )
                    os.remove(f"{file}")
                    break
                else:
                    continue
            await boa.delete()
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["batch"]))
  async def savebatch(bot, message):
       km = message.text.split(" ")[1]
       ms = await message.reply_text("`•Send No. of messages..`.")
       ask_: Message = await bot.listen(message.chat.id, timeout=300)
       if ask_.text:
           mum = int(ask_.text)
           batch.append(message.from_user.id)
           await run_batch(acc, bot, message.from_user.id, km, mum, message)
           batch.clear()
       else:
           await ms.edit("Timeout! 😤")
#########################################
# ping
  @TGBot.on_message(filters.incoming & filters.command(["ping"]))
  async def up(app, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    stt = dt.now()
    ed = dt.now()
    v = TimeFormatter(int((ed - uptime).seconds) * 1000)
    ms = (ed - stt).microseconds / 1000
    p = f"🌋Pɪɴɢ = {ms}ms"
    await message.reply_text(v + "\n" + p)
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["ssgen"]))
  async def ssgen(bot, message):
       numss = message.text.split(" ")[1]
       ms = await message.reply_text("Downloading...")
       reply = message.reply_to_message
       if not reply:
          await ms.edit("Please Reply To An File or video or audio With filename & extension")
          return
       media = reply.document or reply.audio or reply.video
       if not media:
          await ms.edit("Please Reply To An File or video or audio With filename & extension")
       file_size = media.file_size
       c_time = time.time()
       try:
            file_path = await bot.download_media(
                   message=media,
                   progress=progress_for_pyrogram,
                   progress_args=(bot, "` Trying To Download...`", ms, c_time)
            )
       except Exception as e:
               await ms.edit(e)
               return
       width, height, duration = await Mdata01(file_path)
       list_images = await generate_screen_shots(file_path,os.path.dirname(os.path.abspath(file_path)), numss, duration)
       if list_images is None:
            await ms.edit("Failed to get Screenshots!")
       else:
            await ms.edit("Generated Screenshots Successfully!\nNow Uploading ...")
            photo_album = list()
            if list_images is not None:
                    i = 0
                    for image in list_images:
                         if os.path.exists(str(image)):
                               if i == 0:
                                   photo_album.append(InputMediaPhoto(media=str(image)))
                               else:
                                   photo_album.append(InputMediaPhoto(media=str(image)))
                               i += 1
            await bot.send_media_group(
                 chat_id=message.from_user.id,
                 media=photo_album
            )
            try:
                 for pic in photo_album:
                      os.remove(pic)
                 os.remove(list_images)
                 os.remove(file_path)
            except:
                pass
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["gensample"]))
  async def gensample(bot, message):
      ms = await message.reply_text("Downloading...")
      reply = message.reply_to_message
      if not reply:
         await ms.edit("Please Reply To An File or video or audio With filename & extension")
         return
      media = reply.document or reply.audio or reply.video
      if not media:
         await ms.edit("Please Reply To An File or video or audio With filename & extension")
      c_time = time.time()
      try:
           file_path = await bot.download_media(
                  message=media,
                  progress=progress_for_pyrogram,
                  progress_args=(bot, "` Trying To Download...`", ms, c_time)
           )
      except Exception as e:
              await ms.edit(e)
              return
      format = file_path.rsplit(".", 1)[-1].lower()
      width, height, duration = await Mdata01(file_path)
      ttl = int(duration*10 / 100)
      sample_video = await cult_small_video(
          video_file=file_path,
          output_directory=os.path.dirname(os.path.abspath(file_path)),
          start_time=ttl,
          end_time=(ttl + 10),
          format_=format
      )
      if sample_video is None:
            await ms.edit("Failed to Generate Sample Video!")     
      else:
          await ms.edit("Successfully Generated Sample Video!\nNow Uploading ...")
          sam_vid_width, sam_vid_height, sam_vid_duration = await Mdata01(sample_video)
          try:
             await bot.send_video(
                message.from_user.id,
                video=sample_video,            
                width=sam_vid_width,
                height=sam_vid_height,
                duration=sam_vid_duration,
                progress=progress_for_pyrogram,
                progress_args=(bot, "`Trying To Uploading`", ms, c_time)
             )
             await ms.delete()
             os.remove(sample_video)      
             os.remove(file_path)     
          except Exception as e:
                  await ms.edit(e)
                  os.remove(sample_video)
                  os.remove(file_path)
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["trim"]))
  async def trim(bot, message):
    #  ms = await message.reply_text("send me the start time of the video you want to trim from as a reply to this. \n\nIn format hh:mm:ss , for eg: `01:20:69` ")
      start = message.text.split(" ")[1]
      end = message.text.split(" ")[2]
      ms = await message.reply_text("Downloading...")
      reply = message.reply_to_message
      if not reply:
         await ms.edit("Please Reply To An File or video or audio With filename & extension")
         return
      media = reply.document or reply.audio or reply.video
      if not media:
         await ms.edit("Please Reply To An File or video or audio With filename & extension")
      c_time = time.time()
      try:
           file_path = await bot.download_media(
                  message=media,
                  progress=progress_for_pyrogram,
                  progress_args=(bot, "` Trying To Download...`", ms, c_time)
           )
      except Exception as e:
              await ms.edit(e)
              return
      format = file_path.rsplit(".", 1)[-1].lower()
      width, height, duration = await Mdata01(file_path)
      trim_video = await trimmer(
          video_file=file_path,
          output_directory=os.path.dirname(os.path.abspath(file_path)),
          start_time=start,
          end_time=end,
          format_=format
      )
      if trim_video is None:
            await ms.edit("Failed to Generate Trimmed Video!")     
      else:
          await ms.edit("Successfully Trimmed Video!\nNow Uploading ...")
          sam_vid_width, sam_vid_height, sam_vid_duration = await Mdata01(trim_video)
          try:
             await bot.send_video(
                message.from_user.id,
                video=trim_video,            
                width=sam_vid_width,
                height=sam_vid_height,
                duration=sam_vid_duration,
                progress=progress_for_pyrogram,
                progress_args=(bot, "`Trying To Uploading`", ms, c_time)
             )
             await ms.delete()
             os.remove(trim_video)      
             os.remove(file_path)     
          except Exception as e:
                  await ms.edit(e)
                  os.remove(trim_video)
                  os.remove(file_path)
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["status"]))
  async def stats_handler(bot, message):
    tp = dt.now()
    currentTime = TimeFormatter(int((tp - uptime).seconds) * 1000)
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(psutil.net_io_counters().bytes_sent)
    recv = humanbytes(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    ids = getid()
    total_users = len(ids)
    OUT = f"<b>「 💠 BOT STATISTICS 」</b>\n<b>⏳ Bot Uptime : {currentTime}</b>\n<b>💾 Total Disk Space : {total}</b>\n<b>📀 Total Used Space : {used}</b>\n<b>💿 Total Free Space : {free}</b>\n<b>🔺 Total Upload : {sent}</b>\n<b>🔻 Total Download : {recv}</b>\n<b>🖥 CPU : {cpuUsage}%</b>\n<b>⚙️ RAM : {memory}%</b>\n<b>💿 DISK : {disk}%</b>\n\n<b>Total Users in DB: `{total_users}`</b>"         
    await message.reply_text(OUT, quote=True)
#########################################
  @TGBot.on_message(filters.private & filters.reply)
  async def refunc(bot, message):
        if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
            chat_id = message.chat.id
            message_id = message.reply_to_message.id
            new_name = message.text
            await message.delete()
            media = await bot.get_messages(chat_id=chat_id, message_ids=message_id)
            #media = await bot.get_messages(chat_id=chat_id, message_ids=message.reply_to_message.id)
            file = media.reply_to_message.document or media.reply_to_message.video or media.reply_to_message.audio
            filename = file.file_name
            types = file.mime_type.split("/")
            mime = types[0]
            mg_id = media.reply_to_message.id
            try:
                out = new_name.split(".")
                out[1]
                out_name = out[-1]
                out_filename = new_name
                await message.reply_to_message.delete()
                if mime == "video":
                    markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Document", callback_data="doc"),
                                                     InlineKeyboardButton("🎥 Video", callback_data="vid")]])
                elif mime == "audio":
                    markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Document", callback_data="doc"),
                                                     InlineKeyboardButton("🎵 audio", callback_data="aud")]])
                else:
                    markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Document", callback_data="doc")]])
                await message.reply_text(f"**Select the output file type**\n**Output FileName** :- ```{out_filename}```",
                                         reply_to_message_id=mg_id, reply_markup=markup)
            except:
                try:
                    out = filename.split(".")
                    out_name = out[-1]
                    out_filename = new_name + "." + out_name
                except:
                    await message.reply_to_message.delete()
                    await message.reply_text("**Error**: No Extension in File, Not Supporting",
                                             reply_to_message_id=mg_id)
                    return
                await message.reply_to_message.delete()
                if mime == "video":
                    markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Document", callback_data="doc"),
                                                     InlineKeyboardButton("🎥 Video", callback_data="vid")]])
                elif mime == "audio":
                    markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Document", callback_data="doc"),
                                                     InlineKeyboardButton("🎵 audio", callback_data="aud")]])
                else:
                    markup = InlineKeyboardMarkup([[InlineKeyboardButton("📁 Document", callback_data="doc")]])
                await message.reply_text(f"**Select the output file type**\n**Output FileName** :- ```{out_filename}```",
                                         reply_to_message_id=mg_id, reply_markup=markup)
#########################################
  @TGBot.on_message(filters.private & filters.command('set_caption'))
  async def add_caption(bot, message):
    if len(message.command) == 1:
       return await message.reply_text("**__𝙶𝚒𝚟𝚎 𝚖𝚎 𝚊 𝚌𝚊𝚙𝚝𝚒𝚘𝚗 𝚝𝚘 𝚜𝚎𝚝.__\n\n𝙴𝚡𝚊𝚖𝚙𝚕𝚎:- `/set_caption {filename}\n\n💾 Size: {filesize}\n\n⏰ Duration: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await set_caption(message.from_user.id, caption=caption)
    await message.reply_text("__**✅ 𝚈𝙾𝚄𝚁 𝙲𝙰𝙿𝚃𝙸𝙾𝙽 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝚂𝙰𝚅𝙴𝙳**__")
#########################################
  @TGBot.on_message(filters.private & filters.command('del_caption'))
  async def delete_caption(bot, message):
    caption = await get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("__**😔 𝚈𝙾𝚄 𝙳𝙾𝙽𝚃 𝙷𝙰𝚅𝙴 𝙰𝙽𝚈 𝙲𝙰𝙿𝚃𝙸𝙾𝙽**__")
    await set_caption(message.from_user.id, caption=None)
    await message.reply_text("__**❌️ 𝚈𝙾𝚄𝚁 𝙲𝙰𝙿𝚃𝙸𝙾𝙽 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙴𝙻𝙴𝚃𝙴𝙳**__")
#########################################
  @TGBot.on_message(filters.private & filters.command('see_caption'))
  async def see_caption(bot, message):
    caption = await get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**𝚈𝙾𝚄𝚁 𝙲𝙰𝙿𝚃𝙸𝙾𝙽:-**\n\n`{caption}`")
    else:
       await message.reply_text("__**😔 𝚈𝙾𝚄 𝙳𝙾𝙽𝚃 𝙷𝙰𝚅𝙴 𝙰𝙽𝚈 𝙲𝙰𝙿𝙸𝙾𝙽**__")
#########################################
  @TGBot.on_message(filters.private & filters.command('viewthumb'))
  async def viewthumb(bot, message):
     thumb = await get_thumbnail(message.from_user.id)
     if thumb:
       await client.send_photo(chat_id=message.chat.id, photo=thumb)
     else:
        await message.reply_text("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__") 
#########################################
  @TGBot.on_message(filters.private & filters.command('delthumb'))
  async def removethumb(bot, message):
     await set_thumbnail(message.from_user.id, file_id=None)
     await message.reply_text("❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__")
#########################################
  @TGBot.on_message(filters.private & filters.photo)
  async def addthumbs(bot, message):
     dkp = await message.reply_text("Please Wait ...")
     await set_thumbnail(message.from_user.id, file_id=message.photo.file_id)        
     await dkp.edit("✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__")
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["mongo"]))
  async def trim(bot, message):
     dburl = message.text.split(" ")[1]
     dbname = message.text.split(" ")[2]
     COLLECTION_NAME = message.text.split(" ")[3]
     rju = await message.reply('<b>Processing🔰...</b>')
     try:
        mongo = motor.motor_asyncio.AsyncIOMotorClient(dburl)
        db = mongo[dbname]
        col = db.users
        grp = db.groups
        sizes = await db.command("dbstats")['dataSize']
     except Exception as e:
           await rju.edit(f"error {e}")
     instance = Instance.from_db(db)
     @instance.register
     class Media(Document):
          file_id = fields.StrField(attribute='_id')
          file_ref = fields.StrField(allow_none=True)
          file_name = fields.StrField(required=True)
          file_size = fields.IntField(required=True)
          file_type = fields.StrField(allow_none=True)
          mime_type = fields.StrField(allow_none=True)
          caption = fields.StrField(allow_none=True)
          class Meta:
              collection_name = COLLECTION_NAME
     files = await Media.count_documents()
     free = 536870912 - size
     size = get_size(sizes)
     free = get_size(free)
     total_users = await col.count_documents({})
     totl_chats = await grp.count_documents({})
     await rju.edit(Translation.STATUS_TXT.format(files, total_users, totl_chats, size, free))

#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["unzip"]))
  async def unzip(bot, message):
    ms = await message.reply_text("Downloading...")
    user_id = message.from_user.id
    download_path = f"{Config.DOWN_PATH}/{user_id}"
    ext_files_dir = f"{download_path}/extracted"
    if not os.path.isdir(download_path):
              os.makedirs(download_path)
    reply = message.reply_to_message
    if not reply:
       return await ms.edit("Please Reply To An File or video or audio With filename & extension")
    media = reply.document or reply.audio or reply.video
    if not media:
       await ms.edit("Please Reply To An File or video or audio With filename & extension")
    c_time = time.time()
    try:
         archive = await reply.download(
                    file_name=f"{download_path}/{media.file_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "**Trying to Download!**", ms, c_time)
                    )
    except Exception as e:
            await ms.edit(e)
            return
    if len(message.command) == 2:
        passwd = message.text.split(" ")[1]
        extractor = await extr_files(path=ext_files_dir, archive_path=archive, password=passwd)
    else:
        extractor = await extr_files(path=ext_files_dir, archive_path=archive)
    file_path = f"{Config.DOWN_PATH}/{user_id}/extracted"
    paths = get_files(path=file_path)
    if not paths:
            try:
                shutil.rmtree(f"{Config.DOWN_PATH}/{user_id}")
            except:
                pass
    for file in paths:
        try:
            await bot.send_document(
                  chat_id=message.chat.id,
                  document=file,
                  force_document=True,
                  caption="©️ @dhruvprajapati2",
                  reply_to_message_id=message.id,
                  progress=progress_for_pyrogram,
                  progress_args=(bot, "UPLOADING", ms, c_time)
            )
            os.remove(file)
        except FloodWait as f:
            asyncio.sleep(f.x)
            return
        except FileNotFoundError:
            await ms.edit("file not found")
        except BaseException:
           shutil.rmtree(download_path)
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["lastpdf"]))
  async def lstpdf(bot, message):
     ms = await message.reply_text("Okay Send Me The Last Pdf! ♻")
     tmkyt.insert(0, "on")
#########################################
  async def addpdf(bot, message: Message):
     ms = await message.reply_text("Merging Now 🔥!\nplease wait...")
     user_id = message.from_user.id
     download_path = f"{Config.DOWN_PATH}/{user_id}"
     if not os.path.isdir(download_path):
              os.makedirs(download_path)
     for me in pdfiles:
         try:
            media = me.video or me.document
            path = await bot.download_media(
                   message=me,
                   file_name=f"{download_path}/{media.file_name}",
                   progress=progress_for_pyrogram,
                   progress_args=(bot, "``` Trying To Download...```", ms, c_time)
                   )
         except Exception as e:
               await ms.edit(e)
     pdf_files = [file for file in os.listdir(download_path) if file.endswith(".pdf")]
     merger = PdfMerger()
     for pdf_file in pdf_files:
         pdf_path = os.path.join(download_path, pdf_file)
         merger.append(pdf_path)
     output_path = f"{download_path}/merged.pdf"
     merger.write(output_path)
     merger.close()
     await ms.edit("`Merged Successful Now sending you`")
     c_time = time.time()
     try:
            await bot.send_document(
                  chat_id=message.chat.id,
                  document=f"{download_path}/merged.pdf",
                  force_document=True,
                  caption="©️ @dhruvprajapati2",
                  reply_to_message_id=message.id,
                  progress=progress_for_pyrogram,
                  progress_args=(bot, "UPLOADING", ms, c_time)
            )
            shutil.rmtree(download_path)
     except Exception as e:
           await ms.edit(e)
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["lastaud"]))
  async def lstaudio(bot, message):
     ms = await message.reply_text("Okay Send Me The Last Audio! ♻")
     tmkyt.insert(0, "aud")
#########################################
  async def addaudio(bot, message: Message):
     ms = await message.reply_text("Merging Now 🔥!\nplease wait...")
     user_id = message.from_user.id
     download_path = f"{Config.DOWN_PATH}/{user_id}"
     if not os.path.isdir(download_path):
              os.makedirs(download_path)
     for me in audiofiles:
         try:
            media = me.audio
            path = await bot.download_media(
                   message=me,
                   file_name=f"{download_path}/{media.file_name}",
                   progress=progress_for_pyrogram,
                   progress_args=(bot, "` Trying To Download...`", ms, c_time)
            )
         except Exception as e:
               await ms.edit(e)
     audio_files = [file for file in os.listdir(download_path) if file.endswith(".mp3")]
     with open("input.txt", "w") as f:
       for audio_file in audio_files:
         f.write(f"{os.path.join(download_path, audio_file)}")
     subprocess.call([
         "ffmpeg", "-f", "concat", "-safe", "0", "-i", "input.txt", "-c", "copy", "output.mp3"
     ])
     c_time = time.time()
     try:
            await bot.send_document(
                  chat_id=message.chat.id,
                  document=output.mp3,
                  force_document=True,
                  caption="©️ @dhruvprajapati2",
                  reply_to_message_id=message.id,
                  progress=progress_for_pyrogram,
                  progress_args=(bot, "UPLOADING", ms, c_time)
            )
            os.remove("input.txt")
            shutil.rmtree(download_path)
     except Exception as e:
           await ms.edit(e)
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
  async def warn(c, m):
    if len(m.command) >= 3:
        try:
            user_id = m.text.split(' ', 2)[1]
            reason = m.text.split(' ', 2)[2]
            await m.reply_text("User Notified Successfully")
            await c.send_message(chat_id=int(user_id), text=reason)
        except:
            await m.reply_text("User Not Notified Successfully 😔")
#########################################
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
  async def broadcast(bot, message):
    if message.reply_to_message:
        ms = await message.reply_text("Getting All ids from database ...........")
        ids = getid()
        tot = len(ids)
        success = 0
        failed = 0
        await ms.edit(f"Starting Broadcast .... \nSending Message To {tot} Users")
        for id in ids:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(id)
                success += 1
            except:
                failed += 1
                delete({"id": id})
                pass
        try:
            await ms.edit(f"Message sent to {success} chat(s). {failed} chat(s) failed on receiving message. \nTotal - {tot}")
        except FloodWait as e:
            await asyncio.sleep(t.x)
#########################################
#auth
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["auth"]))
  async def auth(bot, message):
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"SUCCESSFULLY ADDED {cr} TO AUTHORISED USERS"
    auth = int(f'{cr}')
    Config.AUTH_USERS.append(auth)
    await message.reply_text(OUT, quote=True)
#########################################
# unauth
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["unauth"]))
  async def unauth(bot, message):
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"SUCCESSFULLY REMOVED {cr} FROM AUTHORISED USERS"
    auth = int(f'{cr}')
    Config.AUTH_USERS.remove(auth)
    await message.reply_text(OUT, quote=True)
#########################################
# users
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["users"]))
  async def users(bot, message):
    ms = await message.reply_text("Getting All ids from database ...........")
    ids = getid()
    tot = len(ids)
    await ms.edit(f"THERE ARE TOTAL {tot} Users In Mongodb Database...")
#########################################
# AUTH_USERS
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["authusers"]))
  async def authuser(bot, message):
    ms = await message.reply_text("Getting All ids in Auth Users...........")
    allows = len(Config.AUTH_USERS)
    await ms.edit(f"THERE ARE TOTAL {allows} USERS IN AUTH USERS.")
#########################################
# list
  @TGBot.on_message(filters.private & filters.user(ADMIN) & filters.command(["list"]))
  async def listing(bot, message):
    ms = await message.reply_text("Listing Queue Files...........")
    listing = myDB.llen("DBQueue")
    await ms.edit(f"There are total {listing} files in the queue.")
#########################################
# restart
  @TGBot.on_message(filters.command("restart"))
  async def re(bot, message):
    if message.chat.id in Config.AUTH_USERS:
        await message.reply_text("•Restarting")
        quit(1)
#########################################
# to change ffmpeg variables 
  @TGBot.on_message(filters.command("crf"))
  async def re(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"I Wɪʟʟ Bᴇ Usɪɴɢ : {cr} Cʀғ"
    crf.insert(0, f'{cr}')
    await message.reply_text(OUT, quote=True)

  @TGBot.on_message(filters.command("quality"))
  async def re(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"I Wɪʟʟ Bᴇ Usɪɴɢ : {cr} Qᴜᴀʟɪᴛy."
    qualityy.insert(0, f'{cr}')
    await message.reply_text(OUT, quote=True)
  
  @TGBot.on_message(filters.command("codec"))
  async def re(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"I Wɪʟʟ Bᴇ Usɪɴɢ : {cr} Cᴏᴅᴇᴄ"
    codec.insert(0, f'{cr}')
    await message.reply_text(OUT, quote=True)
  
  @TGBot.on_message(filters.command("audio"))
  async def re(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    _any = message.text.split(" ", maxsplit=1)[1]
    #OUT = "This feature has been removed.\nLibopus audio codec is replaced by Libfdk_aac.\nIt requires vbr instead of audio bitrates.\nDefault vbr is set to `2`.\nYou don't have to change it."
    #myDB.set('audio', f'{cr}')
    audio_.insert(0, f"{_any}")
    await message.reply_text(f"Fɪɴᴇ! yᴏᴜʀ Fɪʟᴇs Aʀᴇ {_any} Aᴜᴅɪᴏ 👀", quote=True)
  
  @TGBot.on_message(filters.command("resolution"))
  async def re(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    #OUT = f"I have changed my gear to {cr}"
    #myDB.set('speed', f'{cr}')
    OUT = f"<b>I Wɪʟʟ Bᴇ Usɪɴɢ {cr} Qᴜᴀʟɪᴛy Iɴ Rᴇɴᴀᴍɪɴɢ Fɪʟᴇs<b>"
    quality_.insert(0, f"{cr}")
    await message.reply_text(OUT, quote=True)
  
  @TGBot.on_message(filters.command("preset"))
  async def re(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    #OUT = f"I have changed my gear to {cr}"
    #myDB.set('speed', f'{cr}')
    OUT = f"I Wɪʟʟ Bᴇ Usɪɴɢ {cr} Pʀᴇsᴇᴛ Iɴ Eɴᴄᴏᴅɪɴɢ Fɪʟᴇs."
    preset.insert(0, f"{cr}")
    await message.reply_text(OUT, quote=True)
  
# audio_mode ( for libopus and libfdk_aac support )
  @TGBot.on_message(filters.command("audio_codec"))
  async def re_codec_(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    #OUT = f"I have changed my gear to {cr}"
    #myDB.set('speed', f'{cr}')
    OUT = f"<b>I Wɪʟʟ Usᴇ {cr} Aᴜᴅɪᴏ Cᴏᴅᴇᴄ Iɴ Eɴᴄᴏᴅɪɴɢ Fɪʟᴇs.<b>"
    #quality_.insert(0, f"{cr}")
    audio_codec.insert(0, f"{cr}")
    await message.reply_text(OUT, quote=True)
    
# watermark size
  @TGBot.on_message(filters.command("watermark_size"))
  async def re_codec_(bot, message):
    if message.from_user.id not in Config.AUTH_USERS:
        return
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"<b>I Wɪʟʟ Usᴇ {cr} Wᴀᴛᴇʀᴍᴀʀᴋ Sɪᴢᴇ Iɴ Eɴᴄᴏᴅɪɴɢ Fɪʟᴇs.<b>"
    watermark_size.insert(0, f"{cr}")
    await message.reply_text(OUT, quote=True)

# settings
  @TGBot.on_message(filters.incoming & filters.command(["settings"]))
  async def settings(app, message):
    if message.from_user.id in Config.AUTH_USERS:
      await message.reply_text(
        f"🏷 **Video** \n┏━━━━━━━━━━━━━━━━━\n┣ Codec  ➜ ```{codec[0]}```\n┣ **Crf**  ➜ ```{crf[0]}``` \n┣ **Resolution**  ➜ ```{qualityy[0]}```\n┗━━━━━━━━━━━━━━━━━\n\n🏷  **Audio** \n┏━━━━━━━━━━━━━━━━━\n┣ **Codec**  ➜ ```{audio_codec[0]}```\n┣  **Bitrates** ➜ ```{audio_[0]}```\n┗━━━━━━━━━━━━━━━━━\n\n🏷 **Watermark**\n┏━━━━━━━━━━━━━━━━━\n┣ **Position** ➜ ```None```\n┣ **Size**  ➜ ```{watermark_size[0]}```\n┗━━━━━━━━━━━━━━━━━\n\n🏷 **Speed**\n┏━━━━━━━━━━━━━━━━━\n┣ **Preset** ➜ ```{preset[0]}```\n┗━━━━━━━━━━━━━━━━━",
        quote=True
      )

# name
  @TGBot.on_message(filters.incoming & filters.command(["name"]))
  async def settings(app, message):
    if message.from_user.id not in Config.AUTH_USERS:
      return
    cr = message.text.split(" ", maxsplit=1)[1]
    OUT = f"Fɪɴᴇ! I Hᴀᴠᴇ Sᴇᴛ Tʜᴇ Nᴀᴍᴇ Tᴇxᴛ Tᴏ Bᴇ `{cr}` 😃"
    await message.reply_text(OUT, quote=True)
    name.insert(0, f"{cr}")
  # databases
  @TGBot.on_message(filters.incoming & filters.command("clear", prefixes=["/", "."]))
  async def lost_files(bot, message):
    if message.chat.id not in Config.AUTH_USERS:
      return
    #data.clear()
    myDB.delete("DBQueue")
    await message.reply_text("Sᴜᴄᴄᴇssғᴜʟʟy Cʟᴇᴀʀᴇᴅ Qᴜᴇᴜᴇ.", quote=True)
  
  cb_bro = CallbackQueryHandler(
    cb_things
  )
  logger.info("Bot has started successfully 💀✊🏻")
  TGBot.add_handler(cb_bro)
  asyncio.get_event_loop().run_until_complete(start_bot())
