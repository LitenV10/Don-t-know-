import time
import os
import asyncio
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import Client
#from SmartEncoder.Plugins.cb import *
import shutil
from config import Config
from pyrogram.errors import MessageNotModified, FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import subprocess

async def OpenSettings(m: Message, user_id: int):
    try:
        await m.edit(
            text="Here You Can Change or Configure Your Settings:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Show Queue Files", callback_data="showQueueFiles")],
                    [InlineKeyboardButton("Close", callback_data="msgdel")]
                ]
            )
        )
    except MessageNotModified:
        pass
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await m.edit("You Are Spamming!")
    except Exception as err:
        raise err
'''
GAP = {}


async def CheckTimeGap(user_id: int):
    """A Function for checking user time gap!
    :parameter user_id Telegram User ID"""

    if str(user_id) in GAP:
        current_time = time.time()
        previous_time = GAP[str(user_id)]
        if round(current_time - previous_time) < Config.TIME_GAP:
            return True, round(previous_time - current_time + Config.TIME_GAP)
        elif round(current_time - previous_time) >= Config.TIME_GAP:
            del GAP[str(user_id)]
            return False, None
    elif str(user_id) not in GAP:
        GAP[str(user_id)] = time.time()
        return False, None
'''        
async def delete_all(root: str):
    """
    Delete a Folder.

    :param root: Pass Folder Path as String.
    """

    try:
        shutil.rmtree(root)
    except Exception as e:
        print(e)
        
async def MakeButtons(bot: Client, m: Message, db: dict):
    markup = []
    for i in (await bot.get_messages(chat_id=m.chat.id, message_ids=db.get(m.chat.id))):
        media = i.video or i.document or None
        if media is None:
            continue
        else:
            markup.append([InlineKeyboardButton(f"{media.file_name}", callback_data=f"showFileName_{str(i.id)}")])
    markup.append([InlineKeyboardButton("Merge Now", callback_data="mergeNow")])
    markup.append([InlineKeyboardButton("Clear Files", callback_data="cancelProcess")])
    return markup
    
async def fix_thumb(thumb):
    width = 0
    height = 0
    try:
        if thumb != None:
            metadata = extractMetadata(createParser(thumb))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
                Image.open(thumb).convert("RGB").save(thumb)
                img = Image.open(thumb)
                img.resize((320, height))
                img.save(thumb, "JPEG")
    except Exception as e:
        print(e)
        thumb = None 
       
    return width, height, thumb
    
async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None

async def cult_small_video(video_file, output_directory, start_time, end_time, format_):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + str(round(time.time())) + "." + format_.lower()
    file_generator_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    print(t_response)
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None
        
async def generate_screen_shots(video_file, output_directory, no_of_photos, duration):
    images = list()
    ttl_step = duration // no_of_photos
    current_ttl = ttl_step
    for looper in range(no_of_photos):
        await asyncio.sleep(1)
        video_thumbnail = f"{output_directory}/{str(time.time())}.jpg"
        file_generator_command = [
            "ffmpeg",
            "-ss",
            str(round(current_ttl)),
            "-i",
            video_file,
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
        print(e_response)
        print(t_response)
        current_ttl += ttl_step
        images.append(video_thumbnail)
    return images

async def trimmer(video_file, output_directory, start_time, end_time, format_):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + str(round(time.time())) + "." + format_.lower()
    file_generator_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-acodec",
        "copy",
        "-vcodec",
        "copy",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    print(t_response)
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

async def MergeVideo(input_file: str, user_id: int, message: Message, format_: str):
    """
    This is for Merging Videos Together!

    :param input_file: input.txt file's location.
    :param user_id: Pass user_id as integer.
    :param message: Pass Editable Message for Showing FFmpeg Progress.
    :param format_: Pass File Extension.
    :return: This will return Merged Video File Path
    """

    output_vid = f"{Config.DOWN_PATH}/{str(user_id)}/[@AbirHasan2005]_Merged.{format_.lower()}"
    file_generator_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        input_file,
        "-c",
        "copy",
        output_vid
    ]
    process = None
    try:
        process = await asyncio.create_subprocess_exec(
            *file_generator_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except NotImplementedError:
        await message.edit(
            text="Unable to Execute FFmpeg Command! Got `NotImplementedError` ...\n\nPlease run bot in a Linux/Unix Environment."
        )
        await asyncio.sleep(10)
        return None
    await message.edit("Merging Video Now ...\n\nPlease Keep Patience ...")
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    print(t_response)
    if os.path.lexists(output_vid):
        return output_vid
    else:
        return None
        
async def __run_cmds_unzipper(command):
    ext_cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return ext_cmd.stdout.read()[:-1].decode("utf-8")

## Extract with 7z
async def _extract_with_7z_helper(path, archive_path, password=None):
    if password:
        command = f"7z x -o{path} -p{password} {archive_path} -y"
    else:
        command = f"7z x -o{path} {archive_path} -y"
    return await __run_cmds_unzipper(command)

##Extract with zstd (for .zst files)
async def _extract_with_zstd(path, archive_path):
    command = f"zstd -f --output-dir-flat {path} -d {archive_path}"
    return await __run_cmds_unzipper(command)

# Main function to extract files
async def extr_files(path, archive_path, password=None):
    file_path = os.path.splitext(archive_path)[1]
    if file_path != ".zst":
        return await _extract_with_7z_helper(path, archive_path, password)
    os.mkdir(path)
    return await _extract_with_zstd(path, archive_path)

# Get files in directory as a list
def get_files(path):
    path_list = []
    for r, d, f in os.walk(path):
        for file in f:
            path_list.append(os.path.join(r, file))
    return path_list
