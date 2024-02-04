import asyncio

import re
import shlex

import os
async def bash_exec(bot, message):
  cmd = message.text.split(" ", maxsplit=1)[1]
  reply_to_id = message.id
  if message.reply_to_message:
    reply_to_id = message.reply_to_message.id
  oie = await message.reply_text("`Processing...`", quote=True)
  process = await asyncio.create_subprocess_shell(
    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await process.communicate()
  e = stderr.decode()
  if not e:
    e = "No errors"
  o = stdout.decode()
  if not o:
    o = "No output"

  OUTPUT = ""
  OUTPUT += f"<b>Command:</b>\n<code>{cmd}</code>\n\n"
  OUTPUT += f"<b>Output</b>: \n<code>{o}</code>\n"
  OUTPUT += f"<b>Errors</b>: \n<code>{e}</code>"
  
  if len(OUTPUT) > 4096:
    with open("bash.txt", "w+", encoding="utf8") as out_file:
      out_file.write(str(OUTPUT))
    await message.reply_document(
      document="bash.txt",
      caption=f"`{cmd}`",
      reply_to_message_id=message.id,
    )
    await oie.delete()
    os.remove("bash.txt")
  else:
    await bot.edit_message_text(
      chat_id=message.chat.id,
      text=OUTPUT,
      message_id=oie.id #oie.message_id
    )
