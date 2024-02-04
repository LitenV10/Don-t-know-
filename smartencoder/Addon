from config import Config

from SmartEncoder.__main__ import *

from SmartEncoder.Plugins.compress import *


async def d_l(bot, update):
  if update.from_user.id not in Config.AUTH_USERS:
    return
  if update.reply_to_message is None:
    await update.reply_text("Reply to a video file", quote=True)
    return
  if not os.path.isdir(Config.DOWN_PATH):
    os.makedirs(Config.DOWN_PATH)
  doll = Config.DOWN_PATH + "/"
  
  sent_message = await bot.send_message(
    text="**DOWNLOADING**",
    chat_id=update.chat.id,
    reply_to_message_id=update.id #message_id
  )
  c_time = time.time()
  f_n = await bot.download_media(
    message=update.reply_to_message,
    file_name=doll,
    progress=progress_for_pyrogram,
    progress_args=(
      bot,
      "**DOWNLOADING**",
      sent_message,
      c_time
    )
  )
  logger.info(f_n)
  await bot.edit_message_text(
    text=f"Downloaded this file to `{os.path.relpath(f_n,os.getcwd())}`",
    chat_id=update.chat.id,
    message_id=sent_message.id
  )

  
