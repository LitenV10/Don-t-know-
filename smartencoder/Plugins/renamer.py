import logging
import os
import asyncio 
import time
import pickle # to dumps/loads 
import codecs # to encode/decode basically
#import requests
#import json cuz i dont nedd this fucking module
#import urllib3 as url ahh
from datetime import timedelta,datetime
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


from asyncio import sleep
import random
from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from pyrogram.errors import FloodWait
from datetime import datetime as dt
#from SmartEncoder.Plugins.compress import *
# database 
from SmartEncoder.Database.db import *
import SmartEncoder.Plugins.Labour
from SmartEncoder.Plugins.Queue import *
from SmartEncoder.Plugins.list import *
from SmartEncoder.Tools.eval import *
from SmartEncoder.Addons.download import d_l
from SmartEncoder.Addons.executor import bash_exec
from SmartEncoder.Plugins.cb import *
from SmartEncoder.Addons.list_files import l_s
from SmartEncoder.translation import Translation
from SmartEncoder.Tools.progress import *
from config import Config
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from pathlib import Path
from PIL import Image
import humanize
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import anitopy
import os
'''
async def anitopy_renamer(query):
  execute = anitopy.parse(query)
  if 'anime_title' in execute:
    title = execute['anime_title']
  else:
    title = 'Episode'    
  if 'episode_number' in execute:
    episode = execute['episode_number']
  else:
    episode = "Episode"
  if 'video_resolution' in execute:   
    resolution = execute['video_resolution']   
  else:
    resolution = '[720p]'
 # if "AnimeKayo" in title:
    #title_ = title.replace("AnimeKayo", "")
  if episode == "Episode":
    bb = title.replace("S01E", "")
    final = f"{bb} [{quality_[0]}] [{audio_[0]}] @Animes_Encoded.mkv"
   #final = f"{len(rename_queue)} - {title} [480p] [Sub] @AniVoid.mkv"
  else:
    if len(audio_) == 0:
      if len(quality_) == 0:
        final = "{} - {}.mkv".format(episode, title)
    else:
#t = title.replace("Anime Time", "")
      #final = f"{episode} - {title} [{quality_[0]}] [{audio_[0]}] @AniVoid.mkv"
      #ee_ = episode.replace("E", "")
      #t_t = title.replace("-", " ")
      final = f"{title} - {episode}.mkv"
    # final = f"{episode} - Noblesse [480p] [Dual] @AniVoid.mkv"
      #final = "{} - My Dress Up Darling [480p] [Dual] @AniVoid.mkv".format(episode)
      #final = final_.replace("Cleo", "")
    
  path = "downloads/"
  for i in os.listdir(path):
    folder_walk = os.walk(path)
    first_file_in_folder = next(folder_walk)[2][0]
    original = os.path.join(path, first_file_in_folder)
    new = os.path.join(path, final)
    os.rename(original, new)
  return final
    


@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot,update):
	try:
           await update.message.delete()
	except:
           return

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
    #date_fa = str(update.message.date)
	#pattern = '%Y-%m-%d %H:%M:%S'
	#date = int(time.mktime(time.strptime(date_fa, pattern)))
	chat_id = update.message.chat.id
	id = update.message.reply_to_message_id
	await update.message.delete()
	await update.message.reply_text(f"__Please enter the new filename...__\n\nNote:- Extension Not Required",reply_to_message_id = id,
	reply_markup=ForceReply(True) )
	# user_id = update.message.chat.id
	# date = update.message.date
	# await update.message.delete()
	# await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",	
	# reply_to_message_id=update.message.reply_to_message.id,  
	# reply_markup=ForceReply(True))
	

@Client.on_message(filters.private & filters.reply)
async def refunc(client,message):
        if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        	new_name = message.text
        	await message.delete()
        	media = await client.get_messages(message.chat.id,message.reply_to_message.id)
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
        			markup = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("📁 Document",callback_data = "doc"), 
        			InlineKeyboardButton("🎥 Video",callback_data = "vid") ]])
        		elif mime == "audio":
        			markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document",callback_data = "doc")
        			,InlineKeyboardButton("🎵 audio",callback_data = "aud") ]])
        		else:
        			markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document",callback_data = "doc") ]])
        		# dont chenge this message.reply_text     			        		
        		await message.reply_text(f"**Select the output file type**\n**Output FileName** :- ```{out_filename}```",reply_to_message_id=mg_id,reply_markup = markup)
        		
        	except:
        		try:
        			out = filename.split(".")
        			out_name = out[-1]
        			out_filename= new_name + "."+ out_name
        		except:
        			await message.reply_to_message.delete()
        			await message.reply_text("**Error** :  No  Extension in File, Not Supporting"
        			,reply_to_message_id=mg_id)
        			return
        		await message.reply_to_message.delete()
        		if mime == "video":
        			markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document",callback_data = "doc")
        			,InlineKeyboardButton("🎥 Video",callback_data = "vid") ]])
        		elif mime == "audio":
        			markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document",callback_data = "doc")
        			,InlineKeyboardButton("🎵 audio",callback_data = "aud") ]])
        		else:
        			markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document",callback_data = "doc") ]])
        		# dont chenge this message.reply_text 
        		await message.reply_text(f"**Select the output file type**\n**Output FileName** :- ```{out_filename}```",
        		reply_to_message_id=mg_id,reply_markup = markup)
        		
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot,update):
     new_name = update.message.text	
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     ms = await update.message.edit("```Trying To Download...```")
     c_time = time.time()
     try:
     		path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     		
     except Exception as e:
          await ms.edit(e)
          return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     user_id = int(update.message.chat.id)
     try:
         c_caption = await get_caption(update.message.chat.id)
     except:
         pass
     if c_caption:
       # doc_list= ["filename","filesize"]
      #  new_tex = escape_invalid_curly_brackets(c_caption,doc_list)
        caption = c_caption.format(filename=new_filename,filesize=humanbytes(file.file_size))
     else:
        caption = f"**{new_filename}**"
     value = 2
     if value == 2:
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_document(update.from_user.id,document = file_path,caption = caption,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))			
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			return 
     
            
     			     		   		
   		
     		     		     		
@Client.on_callback_query(filters.regex("vid"))
async def vid(bot,update):
     new_name = update.message.text
    # used_ = find_one(update.from_user.id)
   #  used = used_["used_limit"]
  #   date = used_["date"]
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     ms = await update.message.edit("```Trying To Download...```")
     #used_limit(update.from_user.id,file.file_size)
     c_time = time.time()
    # total_used = used + int(file.file_size)
     #used_limit(update.from_user.id,total_used)
     try:
     		path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     		
     except Exception as e:
       #   neg_used = used - int(file.file_size)
        #  used_limit(update.from_user.id,neg_used)
          await ms.edit(e)
          return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     user_id = int(update.message.chat.id)
     #data = find(user_id)
     try:
         c_caption = await get_caption(update.message.chat.id)
     except:
         pass
     #thumb = data[0]
     
     duration = 0     
     metadata = extractMetadata(createParser(file_path))
     if metadata.has("duration"):
         duration = metadata.get('duration').seconds
     if c_caption:
        vid_list = ["filename","filesize","duration"]
        new_tex = escape_invalid_curly_brackets(c_caption,vid_list)
        caption = new_tex.format(filename=new_filename,filesize=humanbytes(file.file_size),duration=timedelta(seconds=duration))
     else:
        caption = f"**{new_filename}**"
     value = 2
     if value == 2:
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_video(update.from_user.id,video = file_path,duration=duration,caption = caption,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))			
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			return 
     
   
   
     			     		     		
@Client.on_callback_query(filters.regex("aud"))
async def aud(bot,update):
     new_name = update.message.text
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
   #  total_used = used + int(file.file_size)
    # used_limit(update.from_user.id,total_used)
     ms = await update.message.edit("```Trying To Download...```")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file , progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     except Exception as e:
     	#neg_used = used - int(file.file_size)
     	#used_limit(update.from_user.id,neg_used)
     	await ms.edit(e)
     	return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     metadata = extractMetadata(createParser(file_path))
     if metadata.has("duration"):
     	duration = metadata.get('duration').seconds
     user_id = int(update.message.chat.id)
     # data = find(user_id)
     c_caption = await get_caption(update.message.chat.id)
     # thumb = data[0]
     if c_caption:
        aud_list = ["filename","filesize","duration"]
        new_tex = escape_invalid_curly_brackets(c_caption,aud_list)
        caption = new_tex.format(filename=new_filename,filesize=humanbytes(file.file_size),duration=timedelta(seconds=duration))
     else:
        caption = f"**{new_filename}**"
     value = 2
     if value == 2:
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_audio(update.message.chat.id,audio = file_path,caption = caption,duration = duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)


@Client.on_callback_query(filters.regex("upload"))
async def doc(bot,update):
     type = update.data.split("_")[1]
     new_name = update.message.text
     new_filename = new_name.split(":-")[1]
     file_path = f"downloads/{new_filename}"
     file = update.message.reply_to_message
     ms = await update.message.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     user_id = int(update.message.chat.id) 
   #  ph_path = None 
     media = getattr(file, file.media.value)
     c_caption = await get_caption(update.message.chat.id)
  #   c_thumb = await db.get_thumbnail(update.message.chat.id)
     if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
         except Exception as e:
             await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
             return 
     else:
         caption = f"**{new_filename}**"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")    
     await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
     c_time = time.time() 
     try:
        if type == "document":
           await bot.send_document(
		    update.message.chat.id,
                    document=file_path,
                  #  thumb=ph_path, 
                    caption=caption, 
                    progress=progress_for_pyrogram,
                    progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time   ))
        elif type == "video": 
            await bot.send_video(
		    update.message.chat.id,
		    video=file_path,
		    caption=caption,
		 #   thumb=ph_path,
		    duration=duration,
		    progress=progress_for_pyrogram,
		    progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time))
        elif type == "audio": 
            await bot.send_audio(
		    update.message.chat.id,
		    audio=file_path,
		    caption=caption,
		  #  thumb=ph_path,
		    duration=duration,
		    progress=progress_for_pyrogram,
		    progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time   )) 
     except Exception as e: 
         await ms.edit(f" Erro {e}") 
         os.remove(file_path)
   #      if ph_path:
   #        os.remove(ph_path)
         return 
     await ms.delete() 
     os.remove(file_path) 
 #    if ph_path:
    #    os.remove(ph_path) 

async def rename_pro(bot, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
                   [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
        
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
                   [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass



async def rename_pro(bot, message):
  if_files = os.path.isdir("downloads/")
  if if_files == True:
   if os.listdir("downloads/") is not None:
    actual_files = os.listdir("downloads/")
    for i in actual_files:
     file_to_delete = "downloads/" + i
     os.remove(file_to_delete)
  download_location = Config.DOWNLOAD_LOCATION + "/"
  sent_message = await bot.send_message(
    text="**DOWNLOADING**",
    chat_id=message.chat.id,
    reply_to_message_id=message.message_id
  )
  c_time = time.time()
  f_n = await bot.download_media(
    message=message,
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
  logger.info(f"Starting to rename {f_n}")
  await asyncio.sleep(1)
  if f_n is not None:
    await sent_message.edit_text("**TRYING TO RENAME**")
    # if not .mkv or.mp4 or .webm
  if f_n.rsplit(".", 1)[-1].lower() not in ["mkv", "mp4", "webm", "avi"]:
    return await sent_message.edit_text("This format isnt allowed , please send only either **MKV** or **MP4** files.")
    # if in .mkv or .mp4
  #  real_file = 
  path = "downloads/"
  folder_walk = os.walk(path)
  first_file_in_folder = next(folder_walk)[2][0]
  _f_n = await anitopy_renamer(first_file_in_folder)
  new_file_name = "downloads/" + _f_n
  
  if _f_n is not None:
    await sent_message.edit_text(f"UPLOADING **{_f_n}** as a doc.")
    upload = await bot.send_document(
      chat_id=message.chat.id,
      document=new_file_name,
      force_document=True,
      caption="©️ @Animes_Encoded",
      reply_to_message_id=message.message_id,
      progress=progress_for_pyrogram,
      progress_args=(bot, "UPLOADING", sent_message, c_time)
    )
      # remove uploaded file as it will free space
    _fn = "/root/encoder/downloads/" + _f_n
    await sent_message.delete()
    os.remove(_fn)

'''


