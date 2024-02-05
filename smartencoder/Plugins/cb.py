#from smartencoder.__main__ import FormtDB, ReplyDB, QueueDB, ytaudio, thumb, yt, yt480p, yt360p, yt240p,ythd
#from smartencoder.Plugins.main import FormtDB, ReplyDB, QueueDB, ytaudio, thumb, yt, yt480p, yt360p, yt240p,ythd
from smartencoder.__main__ import *
from pyrogram.types import CallbackQuery
from humanfriendly import format_timespan
from smartencoder.translation import Translation
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
import psutil
import shutil
import signal
#from smartencoder.Database.db import myDB 
import os
import asyncio 
import time
import pickle # to dumps/loads 
import codecs # to encode/decode basically
#import requests
#import json cuz i dont nedd this fucking module
#import urllib3 as url ahh
from datetime import timedelta,datetime
from asyncio import sleep
import random
from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from smartencoder.Plugins.ffmg import OpenSettings, trimmer, MergeVideo, generate_screen_shots, cult_small_video, take_screen_shot, fix_thumb, MakeButtons, delete_all, extr_files, get_files
#from smartencoder.Plugins.ffmg import delete_all
from pyrogram.errors import FloodWait
from datetime import datetime as dt
#from smartencoder.Plugins.compress import *
# database 
from smartencoder.Database.db import *
import smartencoder.Plugins.Labour
from smartencoder.Plugins.Queue import *
#from smartencoder.Plugins.ffmpeg import take_screen_shot,fix_thumb
from smartencoder.Plugins.list import *
from smartencoder.Tools.eval import *
from smartencoder.Addons.download import d_l
from smartencoder.Addons.executor import bash_exec
from smartencoder.Plugins.cb import *
from smartencoder.Addons.list_files import l_s
from smartencoder.translation import Translation
from smartencoder.Tools.progress import *
from config import Config
from pyrogram import filters, Client, idle, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from pathlib import Path
from PIL import Image
import humanize
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import anitopy
import os
from smartencoder.Database.set import escape_invalid_curly_brackets


      
async def cb_things(bot, update: CallbackQuery):
  if update.data == "hilp":
    await update.message.edit_text(
      text=Translation.HELP_TEXT,
      parse_mode=enums.ParseMode.MARKDOWN,
      reply_markup=InlineKeyboardMarkup(
        [
          [
            InlineKeyboardButton("🔙", callback_data="beck")],
        ],
      )
    )
  elif update.data == "beck":
    await update.message.edit_text(
      text=Translation.START_TEXT, 
      parse_mode=enums.ParseMode.MARKDOWN,
      reply_markup=InlineKeyboardMarkup(
        [
          [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="hilp")],
        ],
      )
    )
  elif update.data == "rename":
        chat_id = update.message.chat.id
        id = update.message.reply_to_message.id
        await update.message.delete()
        await update.message.reply_text(
            f"__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",
            reply_to_message_id=id,
            reply_markup=ForceReply(True)
        )
    
  elif update.data == "doc":
        new_name = update.message.text
        name = new_name.split(":-")
        new_filename = name[1]
        file_path = f"downloads/{new_filename}"
       
       # message_id = update.message.reply_to_message.message_id
       # message = await bot.get_messages(update.message.chat.id, message_ids=message_id)
        message = update.message.reply_to_message
        file = message.document or message.video or message.audio
        ms = await update.message.edit("`Trying To Download...`")
        c_time = time.time()
        try:
            path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=(bot, "`Downloading...`", ms, c_time)
            )
        except Exception as e:
            await ms.edit(e)
            return
        splitpath = path.split("/downloads/")
        dow_file_name = splitpath[1]
        old_file_name = f"downloads/{dow_file_name}"
        os.rename(old_file_name, file_path)
        user_id = int(update.message.chat.id)
        try:
            c_caption = await get_caption(update.message.chat.id)
        except:
            pass
        try:
            c_thumb = await get_thumbnail(update.message.chat.id)
        except:
               pass
        if c_caption:
            doc_list = ["filename", "filesize"]
            new_tex = escape_invalid_curly_brackets(c_caption, doc_list)
            caption = new_tex.format(
                filename=new_filename, filesize=humanbytes(file.file_size)
            )
        else:
            caption = f"**{new_filename}**"
        if c_thumb:
                ph_path = await bot.download_media(thumb)
                Image.open(ph_path).convert("RGB").save(ph_path)
                img = Image.open(ph_path)
                img.resize((320, 320))
                img.save(ph_path, "JPEG")
                c_time = time.time()
        else:
            ph_path = None
        value = 2
        if value == 2:
            await ms.edit("`Trying To Upload`")
            c_time = time.time()
            try:
                await bot.send_document(
                    update.from_user.id,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading`", ms, c_time)
                )
                await ms.delete()
                os.remove(file_path)
                try:
                   os.remove(ph_path)
                except:
                   pass
            except Exception as e:
                await ms.edit(e)
                os.remove(file_path)
                try:
                   os.remove(ph_path)
                except:
                   return
             
                
  elif update.data == "vid":
        new_name = update.message.text
        name = new_name.split(":-")
        new_filename = name[1]
        file_path = f"downloads/{new_filename}"
        message = update.message.reply_to_message
        # message_id = update.message.reply_to_message.message_id
        # message = await bot.get_messages(update.message.chat.id, message_ids=message_id)
        file = message.document or message.video or message.audio
        #file = message.document or message.video or message.audio
        ms = await update.message.edit("`Trying To Download...`")
        c_time = time.time()
        try:
            path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=(bot, "`Downloading...`", ms, c_time)
            )
        except Exception as e:
            await ms.edit(e)
            return
        splitpath = path.split("/downloads/")
        dow_file_name = splitpath[1]
        old_file_name = f"downloads/{dow_file_name}"
        os.rename(old_file_name, file_path)
        user_id = int(update.message.chat.id)
        try:
            c_caption = await get_caption(update.message.chat.id)
        except:
            pass
        try:
            c_thumb = await get_thumbnail(update.message.chat.id)
        except:
               pass
        duration = 0
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if c_caption:
            vid_list = ["filename", "filesize", "duration"]
            new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
            caption = new_tex.format(
                filename=new_filename,
                filesize=humanbytes(file.file_size),
                duration=timedelta(seconds=duration)
            )
        else:
            caption = f"**{new_filename}**"
        if c_thumb:
                ph_path = await bot.download_media(thumb)
                Image.open(ph_path).convert("RGB").save(ph_path)
                img = Image.open(ph_path)
                img.resize((320, 320))
                img.save(ph_path, "JPEG")
                c_time = time.time()
        else:
            try:
                ph_path_ = await take_screen_shot(file_path,os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                width, height, ph_path = await fix_thumb(ph_path_)
            except Exception as e:
                ph_path = None
                print(e)
        value = 2
        if value == 2:
            await ms.edit("`Trying To Upload`")
            c_time = time.time()
            try:
                await bot.send_video(
                    update.from_user.id,
                    video=file_path,
                    thumb=ph_path,
                    duration=duration,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading`", ms, c_time)
                )
                await ms.delete()
                os.remove(file_path)
                try:
                   os.remove(ph_path)
                except:
                    pass
            except Exception as e:
                await ms.edit(e)
                os.remove(file_path)
                try:
                   os.remove(ph_path)
                except:
                      return
                
  elif update.data == "aud":
        new_name = update.message.text
        name = new_name.split(":-")
        new_filename = name[1]
        file_path = f"downloads/{new_filename}"
        message = update.message.reply_to_message
        # message_id = update.message.reply_to_message.message_id
        # message = await bot.get_messages(update.message.chat.id, message_ids=message_id)
        file = message.document or message.video or message.audio
        #file = message.document or message.video or message.audio
        ms = await update.message.edit("`Trying To Download...`")
        c_time = time.time()
        try:
            path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=(bot, "`Downloading...`", ms, c_time)
            )
        except Exception as e:
            await ms.edit(e)
            return
        splitpath = path.split("/downloads/")
        dow_file_name = splitpath[1]
        old_file_name = f"downloads/{dow_file_name}"
        os.rename(old_file_name, file_path)
        duration = 0
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        user_id = int(update.message.chat.id)
        c_caption = await get_caption(update.message.chat.id)
        if c_caption:
            aud_list = ["filename", "filesize", "duration"]
            new_tex = escape_invalid_curly_brackets(c_caption, aud_list)
            caption = new_tex.format(
                filename=new_filename,
                filesize=humanbytes(file.file_size),
                duration=timedelta(seconds=duration)
            )
        else:
            caption = f"**{new_filename}**"
        value = 2
        if value == 2:
            await ms.edit("`Trying To Upload`")
            c_time = time.time()
            try:
                await bot.send_audio(
                    update.message.chat.id,
                    audio=file_path,
                    caption=caption,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading...`", ms, c_time)
                )
                await ms.delete()
                os.remove(file_path)
            except Exception as e:
                await ms.edit(e)
                os.remove(file_path)
                
  elif update.data == "mergeNow":
        vid_list = list()
        await update.message.edit(
            text="Please Wait ..."
        )
        duration = 0
        list_message_ids = QueueDB.get(update.from_user.id, None)
        list_message_ids.sort()
        input_ = f"{Config.DOWN_PATH}/{update.from_user.id}/input.txt"
        if list_message_ids is None:
            await update.answer("Queue Empty!", show_alert=True)
            await update.message.delete(True)
            return
        if len(list_message_ids) < 2:
            await update.answer("Only One Video You Sent for Merging!", show_alert=True)
            await update.message.delete(True)
            return
        if not os.path.exists(f"{Config.DOWN_PATH}/{update.from_user.id}/"):
            os.makedirs(f"{Config.DOWN_PATH}/{update.from_user.id}/")
        for i in (await bot.get_messages(chat_id=update.from_user.id, message_ids=list_message_ids)):
            media = i.video or i.document
            try:
                await update.message.edit(
                    text=f"Downloading `{media.file_name}` ..."
                )
            except MessageNotModified:
                QueueDB.get(update.from_user.id).remove(i.id)
                await update.message.edit("File Skipped!")
                await asyncio.sleep(3)
                continue
            file_dl_path = None
            try:
                c_time = time.time()
                file_dl_path = await bot.download_media(
                    message=i,
                    file_name=f"{Config.DOWN_PATH}/{update.from_user.id}/{i.id}/",
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "Downloading ...",
                        update.message,
                        c_time
                    )
                )
            except Exception as downloadErr:
                print(f"Failed to Download File!\nError: {downloadErr}")
                QueueDB.get(update.from_user.id).remove(i.id)
                await update.message.edit("File Skipped!")
                await asyncio.sleep(3)
                continue
            metadata = extractMetadata(createParser(file_dl_path))
            try:
                if metadata.has("duration"):
                    duration += metadata.get('duration').seconds
                vid_list.append(f"file '{file_dl_path}'")
            except:
                await delete_all(root=f"{Config.DOWN_PATH}/{update.from_user.id}/")
                QueueDB.update({update.from_user.id: []})
                FormtDB.update({update.from_user.id: None})
                await update.message.edit("Video Corrupted!\nTry Again Later.")
                return
        __cache = list()
        for i in range(len(vid_list)):
            if vid_list[i] not in __cache:
                __cache.append(vid_list[i])
        vid_list = __cache
        if (len(vid_list) < 2) and (len(vid_list) > 0):
            await update.message.edit("There only One Video in Queue!\nMaybe you sent same video multiple times.")
            return
        await update.message.edit("Trying to Merge Videos ...")
        with open(input_, 'w') as _list:
            _list.write("\n".join(vid_list))
        merged_vid_path = await MergeVideo(
            input_file=input_,
            user_id=update.from_user.id,
            message=update.message,
            format_=FormtDB.get(update.from_user.id, "mkv")
        )
        if merged_vid_path is None:
            await update.message.edit(
                text="Failed to Merge Video!"
            )
            await delete_all(root=f"{Config.DOWN_PATH}/{update.from_user.id}/")
            QueueDB.update({update.from_user.id: []})
            FormtDB.update({update.from_user.id: None})
            return
        await update.message.edit("Successfully Merged Video!")
        file_size = os.path.getsize(merged_vid_path)
        if int(file_size) > 2097152000:
            await update.message.edit(f"Sorry Sir,\n\nFile Size Become {humanbytes(file_size)} !!\nI can't Upload to Telegram!\n\nSo Now Uploading to Streamtape ...")
            await UploadToStreamtape(file=merged_vid_path, editable=update.message, file_size=file_size)
            await delete_all(root=f"{Config.DOWN_PATH}/{update.from_user.id}/")
            QueueDB.update({update.from_user.id: []})
            FormtDB.update({update.from_user.id: None})
            return
        await update.message.edit(
            text="Do you like to rename file?\nChoose a Button from below:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Rename File", callback_data="renameFile_Yes")],
                    [InlineKeyboardButton("Keep Default", callback_data="renameFile_No")]
                ]
            )
        )
            
  elif update.data == "cancelProcess":
        await update.message.edit("Trying to Delete Working DIR ...")
        QueueDB.update({update.from_user.id: []})
        FormtDB.update({update.from_user.id: None})
        await update.message.edit("Successfully Cancelled!")
        await delete_all(root=f"{Config.DOWN_PATH}/{update.from_user.id}/")
        
        
  elif update.data.startswith("showFileName_"):
        message_ = await bot.get_messages(chat_id=update.message.chat.id, message_ids=int(update.data.split("_", 1)[-1]))
        try:
            await bot.send_message(
                chat_id=update.message.chat.id,
                text="This File Sir!",
                reply_to_message_id=message_.id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Remove File", callback_data=f"removeFile_{str(message_.id)}")]
                    ]
                )
            )
        except FloodWait as e:
            await update.answer("Don't Spam Unkil!", show_alert=True)
            await asyncio.sleep(e.x)
        except:
            media = message_.video or message_.document
            await update.answer(f"Filename: {media.file_name}")
            
  elif update.data == "showQueueFiles":
        try:
            markup = await MakeButtons(bot, update.message, QueueDB)
            await update.message.edit(
                text="Here are the saved files list in your queue:",
                reply_markup=InlineKeyboardMarkup(markup)
            )
        except ValueError:
            await update.answer("Your Queue Empty Unkil!", show_alert=True)
            
  elif update.data == "openSettings":
        await OpenSettings(update.message, update.from_user.id)
        
  elif update.data.startswith("removeFile_"):
        if (QueueDB.get(update.from_user.id, None) is not None) or (QueueDB.get(update.from_user.id) != []):
            QueueDB.get(update.from_user.id).remove(int(update.data.split("_", 1)[-1]))
            await update.message.edit(
                text="File removed from queue!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Go Back", callback_data="openSettings")]
                    ]
                )
            )
        else:
            await update.answer("Sorry Unkil, Your Queue is Empty!", show_alert=True)
            
  elif update.data.startswith("renameFile_"):
        if (QueueDB.get(update.from_user.id, None) is None) or (QueueDB.get(update.from_user.id) == []):
            await update.answer("Sorry Unkil, Your Queue is Empty!", show_alert=True)
            return
        merged_vid_path = f"{Config.DOWN_PATH}/{str(update.from_user.id)}/[@AbirHasan2005]_Merged.{FormtDB.get(update.from_user.id).lower()}"
        if update.data.split("_", 1)[-1] == "Yes":
            await update.message.edit("Okay Unkil,\nSend me new file name!")
            try:
                ask_: Message = await bot.listen(update.message.chat.id, timeout=300)
                if ask_.text:
                    ascii_ = e = ''.join([i if (i in string.digits or i in string.ascii_letters or i == " ") else "" for i in ask_.text])
                    new_file_name = f"{Config.DOWN_PATH}/{str(update.from_user.id)}/{ascii_.replace(' ', '_').rsplit('.', 1)[0]}.{FormtDB.get(update.from_user.id).lower()}"
                    await update.message.edit(f"Renaming File Name to `{new_file_name.rsplit('/', 1)[-1]}`")
                    os.rename(merged_vid_path, new_file_name)
                    await asyncio.sleep(2)
                    merged_vid_path = new_file_name
            except TimeoutError:
                await update.message.edit("Time Up!\nNow I will upload file with default name.")
            except:
                pass
        await update.message.edit("Extracting Video Data ...")
        duration = 1
        width = 100
        height = 100
        try:
            metadata = extractMetadata(createParser(merged_vid_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
        except:
            await delete_all(root=f"{Config.DOWN_PATH}/{update.from_user.id}/")
            QueueDB.update({update.from_user.id: []})
            FormtDB.update({update.from_user.id: None})
            await update.message.edit("The Merged Video Corrupted!\nTry Again Later.")
            return
        video_thumbnail = None
        db_thumbnail = await get_thumbnail(update.from_user.id)
        if db_thumbnail is not None:
            video_thumbnail = await bot.download_media(message=db_thumbnail, file_name=f"{Config.DOWN_PATH}/{str(update.from_user.id)}/thumbnail/")
            Image.open(video_thumbnail).convert("RGB").save(video_thumbnail)
            img = Image.open(video_thumbnail)
            img.resize((width, height))
            img.save(video_thumbnail, "JPEG")
        else:
            video_thumbnail = Config.DOWN_PATH + "/" + str(update.from_user.id) + "/" + str(time.time()) + ".jpg"
            ttl = random.randint(0, int(duration) - 1)
            file_generator_command = [
                "ffmpeg",
                "-ss",
                str(ttl),
                "-i",
                merged_vid_path,
                "-vframes",
                "1",
                video_thumbnail
            ]
            process = await asyncio.create_subprocess_exec(
                *file_generator_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            t_response = stdout.decode().strip()
            if video_thumbnail is None:
                video_thumbnail = None
            else:
                Image.open(video_thumbnail).convert("RGB").save(video_thumbnail)
                img = Image.open(video_thumbnail)
                img.resize((width, height))
                img.save(video_thumbnail, "JPEG")
        file_size = os.path.getsize(merged_vid_path)
        try:
           sent_ = None
           c_time = time.time()
           sent_ = await bot.send_video(
                chat_id=update.message.chat.id,
                video=merged_vid_path,
                width=width,
                height=height,
                duration=duration,
                thumb=video_thumbnail,
                caption=Config.CAPTION.format((await bot.get_me()).username) + f"\n\n**File Name:** `{merged_vid_path.rsplit('/', 1)[-1]}`\n**Duration:** `{format_timespan(duration)}`\n**File Size:** `{humanbytes(file_size)}`",
                progress=progress_for_pyrogram,
                progress_args=(bot, "Uploading Video ...", update.message, c_time)
           )
        except Exception as e:
                await update.message.edit(e)
        caption = f"© @{(await bot.get_me()).username}"
        m = 2
        if m == 2:
            await update.message.edit("Now Generating Screenshots ...")
            generate_ss_dir = f"{Config.DOWN_PATH}/{str(update.from_user.id)}"
            list_images = await generate_screen_shots(merged_vid_path, generate_ss_dir, 9, duration)
            if list_images is None:
                await update.message.edit("Failed to get Screenshots!")
            else:
                await update.message.edit("Generated Screenshots Successfully!\nNow Uploading ...")
                photo_album = list()
                if list_images is not None:
                    i = 0
                    for image in list_images:
                        if os.path.exists(str(image)):
                            if i == 0:
                                photo_album.append(InputMediaPhoto(media=str(image), caption=caption))
                            else:
                                photo_album.append(InputMediaPhoto(media=str(image)))
                            i += 1
                await bot.send_media_group(
                    chat_id=update.from_user.id,
                    media=photo_album
                )    
        await update.message.delete(True)
        await delete_all(root=f"{Config.DOWN_PATH}/{update.from_user.id}/")
        QueueDB.update({update.from_user.id: []})
        FormtDB.update({update.from_user.id: None})
        
  elif update.data == "audio":
        download = ytaudio.download(filename=f"{str(yt.title)}")
        rem = os.rename(download, f"{str(yt.title)}.mp3")
        c_time = time.time()
        await bot.send_audio(
            update.message.chat.id,
            audio=rem,
            caption="© @dhruvprajapati2",
            duration=yt.length,
            progress=progress_for_pyrogram,
            progress_args=(bot, "`Uploading...`", update.message, c_time)
        )
        await update.message.delete()
        os.remove(rem)
        
  elif update.data == "240p":
        try:
                rem = yt240p.download()
                c_time = time.time()
                await bot.send_video(
                    update.message.chat.id,
                    audio=rem,
                    caption="© @dhruvprajapati2",
                    duration=yt.length,
                    thumb=thumb,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading...`", update.message, c_time)
                )
                await update.message.delete()
                os.remove(rem)
        except Exception as e:
                await bot.send_message(
                  chat_id = update.message.chat.id,
                  text="**😔 240P QUALITY IS NOT AVAILABLE FOR THIS VIDEO\n CHOOSE ANY OTHER QUALITIES**"
                )
  
  elif update.data == "360p":
        try:
                rem = yt360p.download()
                c_time = time.time()
                await bot.send_video(
                    update.message.chat.id,
                    audio=rem,
                    caption="© @dhruvprajapati2",
                    duration=yt.length,
                    thumb=thumb,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading...`", update.message, c_time)
                )
                await update.message.delete()
                os.remove(rem)
        except Exception as e:
                await bot.send_message(
                  chat_id = update.message.chat.id,
                  text="**😔 360P QUALITY IS NOT AVAILABLE FOR THIS VIDEO\n CHOOSE ANY OTHER QUALITIES**"
                )

  elif update.data == "480p":
        try:
                rem = yt480p.download()
                c_time = time.time()
                await bot.send_video(
                    update.message.chat.id,
                    audio=rem,
                    caption="© @dhruvprajapati2",
                    duration=yt.length,
                    thumb=thumb,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading...`", update.message, c_time)
                )
                await update.message.delete()
                os.remove(rem)
        except Exception as e:
                await bot.send_message(
                  chat_id = update.message.chat.id,
                  text="**😔 480P QUALITY IS NOT AVAILABLE FOR THIS VIDEO\n CHOOSE ANY OTHER QUALITIES**"
                )

  elif update.data == "high":
        try:
                rem = ythd.download()
                c_time = time.time()
                await bot.send_video(
                    update.message.chat.id,
                    audio=rem,
                    caption="© @dhruvprajapati2",
                    duration=yt.length,
                    thumb=thumb,
                    progress=progress_for_pyrogram,
                    progress_args=(bot, "`Uploading...`", update.message, c_time)
                )
                await update.message.delete()
                os.remove(rem)
        except Exception as e:
                await bot.send_message(
                  chat_id = update.message.chat.id,
                  text="**😔 1080P QUALITY IS NOT AVAILABLE FOR THIS VIDEO\n CHOOSE ANY OTHER QUALITIES**"
                )

  elif update.data == 'thumbnail':
        await bot.send_photo(
            chat_id = update.message.chat.id, 
            photo=thumb,
            caption="**JOIN @HKBOTZ**"
        )
        await update.message.delete()

  elif update.data == "msgdel":
        if update.from_user.id in Config.AUTH_USERS:
            try:
              await update.message.delete()     
            except:
                pass
            return         
            
  elif update.data == "cancel":
        if update.from_user.id in Config.AUTH_USERS:
            try:
              await update.message.delete()
              for proc in psutil.process_iter():
                processName = proc.name()
                processID = proc.pid
                if processName == "ffmpeg":
                   os.kill(processID, signal.SIGKILL)
                   #myDB.lpop("DBQueue")
            except:
                pass
            return
    
