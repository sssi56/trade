import os
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("API")

API_KEY = os.getenv('WEATHER_API_KEY', API)
BASE_URL = "https://api.weatherapi.com/v1/current.json"
# http://api.weatherapi.com/v1/current.json?key=c3b010247ec84f1b9bf120135252108&q=London&aqi=no
