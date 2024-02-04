from config import Config
import re
from SmartEncoder.__main__ import *
from SmartEncoder.Tools.progress import *

from typing import Tuple, List, Optional, Iterator, Union

from os.path import (
  join, 
  splitext, 
  basename, 
  dirname, 
  relpath, 
  exists, 
  isdir, 
  isfile
)
from pathlib import Path
from SmartEncoder.Plugins.compress import *

  
async def l_s(bot, message):
  cat = "".join(message.text.split(maxsplit=1)[1:])
  path = cat or os.getcwd()
  if not os.path.exists(path):
    await message.reply_text(f"There is no `{cat}` to show as it doesnt exist.", quote=True)
    return
  path = Path(cat) if cat else os.getcwd()
  if os.path.isdir(path):
    if cat:
      msg = "Folders and Files in `{}` :\n".format(path)
    else:
      msg = "Folders and Files in Current Directory :\n"
    lists = os.listdir(path)
    files = ""
    folders = ""
    for contents in sorted(lists):
      catpath = os.path.join(path, contents)
      if not os.path.isdir(catpath):
        size = os.stat(catpath).st_size
        if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
          files += "🔊" + f"{contents}\n"
        if str(contents).endswith((".opus")):
          files += "🎙" + f"{contents}\n"
        elif str(contents).endswith(
          (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            files += "🎥" + f"{contents}\n"
        elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
          files += "🗜" + f"{contents}\n"
        elif str(contents).endswith(
          (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            files += "🖼" + f"{contents}\n"
        else:
          files += "📒" + f"{contents}\n"
      else:
        folders += f"📁{contents}\n"
    msg = msg + folders + files if files or folders else msg + "Empty Path"
  else:
    size = os.stat(path).st_size
    msg = "The details of given file :\n"
    if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
      mode = "🔊"
    if str(path).endswith((".opus")):
      mode = "🎙"
    elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
      mode = "🎥"
    elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
      mode = "🗜"
    elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
      mode = "🖼"
    else:
      mode = "📄"
    time.ctime(os.path.getctime(path))
    time2 = time.ctime(os.path.getmtime(path))
    time3 = time.ctime(os.path.getatime(path))
    msg += f"**Location :** `{path}`\n"
    msg += f"**icon :** `{mode}`\n"
    msg += f"**Size :** `{humanbytes(size)}`\n"
    msg += f"**Last Modified Time:** `{time2}`\n"
    msg += f"**Last Accessed Time:** `{time3}`"
    
    
    
    
  await message.reply_text(msg, quote=True)
