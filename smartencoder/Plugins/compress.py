# encode.py> 

import asyncio
import os
import time
import subprocess
import math
import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from smartencoder.plugins.list import *

from smartencoder.Tools.progress import *
from smartencoder.Tools.ffmpeg_progress import progress_shell
#from smartencoder.Database.db import myDB


async def en_co_de(dl, message):
  pron = dl.split("/")[-1]
  sox = pron.split(".")[-1]
  ul = pron.replace(f".{sox}", ".mkv")
  TF = time.time()
  progress = f"progress-{TF}.txt"
  # ffmpeg encoding code 
  if codec[0] == "libx265":
    if audio_codec[0] == "libfdk_aac":
      cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -map 0:v? -map 0:a? -map 0:s? -c:v libx265 -x265-params no-info=1 -crf {crf[0]} -s {qualityy[0]} -b:v 420k  -preset {preset[0]} -threads 3 -pix_fmt yuv420p -c:a libfdk_aac -profile:a aac_he_v2 -ac 2 -vbr 1 -c:s copy """{ul}""" -y'''
    elif audio_codec[0] == "libopus":
      cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -filter_complex "drawtext=fontfile=njnaruto(1).ttf:fontsize={watermark_size[0]}:fontcolor=white:bordercolor=black@0.50:x=10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text='DKP':enable='between(t,0,15)':alpha='if(lt(t,14)\,1\,if(lt(t\,15)\,(1-(t-14))/1\,0))'" -metadata:s:a:0 title="[Telegram @dhruvprajapati2]" -metadata:s:a:1 title="[Telegram @dhruvprajapati2]" -metadata:s:s:0 title="[Telegram @dhruvprajapati2]" -metadata:s:s:1 title="[Telegram @dhruvprajapati2]" -map 0:v? -map 0:a? -map 0:s? -c:v libx265 -x265-params no-info=1 -crf {crf[0]} -s {qualityy[0]} -b:v 420k -preset {preset[0]} -threads 3 -pix_fmt yuv420p -c:a libopus -profile:a aac_he -ac 2 -b:a {audio_[0]} -c:s copy """{ul}""" -y'''
  else:
    if audio_codec[0] == "libopus":
      cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -map 0:a? -map 0:s? -map 0:v? -c:v libx264 -crf {crf[0]} -pix_fmt yuv420p -s {qualityy[0]} -preset {preset[0]} -c:a libopus -profile:a aac_he -ac 2 -b:a {audio_[0]} -c:s copy """{ul}""" -y'''
    elif audio_codec[0] == "libfdk_aac":
      cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -map 0:a? -map 0:s? -map 0:v? -c:v libx264 -crf {crf[0]} -pix_fmt yuv420p -s {qualityy[0]} -preset {preset[0]} -c:a libfdk_aac -profile:a aac_he_v2 -ac 2 -vbr 1 -c:s copy """{ul}""" -y'''
  # bot pm info for process -_-
  await progress_shell(cmd, dl, progress, TF, message, "**ENCODING IN PROGRESS**")
  if os.path.lexists(ul):
    return ul
  else:
    return None
  
# (c) Animes_Encoded
