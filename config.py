import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
BOT_TOKEN = os.environ["TOKEN"]
BASE_DIR = Path(__file__).resolve().parent