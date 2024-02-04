import logging
from logging.handlers import RotatingFileHandler
import os
import time
from pyrogram import Client
from config import Config 


TGBot = Client(
  "bot_mode",
  bot_token=Config.BOT_TOKEN,
  api_id=Config.API_ID,
  api_hash=Config.API_HASH,
  workers=100
)



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.getLogger("pyrogram").setLevel(logging.WARNING)
