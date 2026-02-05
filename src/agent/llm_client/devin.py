# import os
# import requests
# from dotenv import load_dotenv
# from typing import Optional, Dict, Any

# load_dotenv()

# DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")
# # DEVIN_BASE_URL = "https://api.devin.ai/v1"
# DEVIN_BASE_URL = "https://api.devin.ai/v1/sessions"

# response = requests.post(
#     url=DEVIN_BASE_URL,
#     headers={"Authorization": f"Bearer {DEVIN_API_KEY}"},
#     json={
#         "prompt": "我现在使用的是哪些仓库"
#     }
# )

# print(response.json())
from openai import OpenAI  
  
client = OpenAI()  
  
