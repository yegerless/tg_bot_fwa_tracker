import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OW_API_KEY = os.getenv('OW_API_KEY')    # OpenWeather API KEY
# NIX_API_ID = os.getenv('NIX_API_ID')
# NIX_API_KEY = os.getenv('NIX_API_KEY')
NINJAS_API_KEY = os.getenv('NINJAS_API_KEY')
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_API_KEY = os.getenv('EDAMAM_API_KEY')
