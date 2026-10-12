import os
import requests
from dotenv import load_dotenv
load_dotenv()
webhook_url = os.getenv("SLACK_WEBHOOK_URL")
response = requests.post(webhook_url, json={"text": "こんにちは"},timeout=30)
print(response.status_code)