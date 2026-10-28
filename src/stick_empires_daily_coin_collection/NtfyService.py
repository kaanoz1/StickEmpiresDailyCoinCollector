import os
import asyncio
import logging
import requests
from dotenv import load_dotenv

logger = logging.getLogger("StickEmpiresLoop")

load_dotenv()

NTFY_TOPIC_NAME = os.getenv("NTFY_TOPIC_NAME")

if NTFY_TOPIC_NAME is None:
    raise ValueError("NTFY_TOPIC_NAME environment variable is not set. Please set it in the .env file.")


class NtfyService:
    @staticmethod
    async def send_notification(title: str, message: str) -> None:
        """
        Asynchronously sends a notification to the specified ntfy.sh topic.
        Retries indefinitely every 5 seconds if a network failure occurs.
        """
        url = f"https://ntfy.sh/{NTFY_TOPIC_NAME}"
        headers = {"Title": title.encode("utf-8")}  # Safe encoding for emojis/special chars

        while True:
            try:
                response = requests.post(
                    url,
                    data=message.encode("utf-8"),
                    headers=headers,
                    timeout=10
                )
                
                response.raise_for_status() 
                break  
            except requests.exceptions.RequestException as e:
                logger.warning(f"Failed to send ntfy notification: {e}. Retrying in 5 seconds...")
                
                await asyncio.sleep(5)
