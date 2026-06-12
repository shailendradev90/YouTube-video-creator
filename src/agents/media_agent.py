import os
from dotenv import load_dotenv
from src.services.pixels_service import PexelsService


load_dotenv()
pexels = PexelsService(os.getenv("PEXELS_API_KEY"))

def download_media(topic):
  
 return pexels.search_and_download(topic)