import os

from dotenv import load_dotenv

SERVER_IP: str = "23.23.246.201"
PORT: int = 9933

load_dotenv()

message = os.getenv("LOGIN_MESSAGE_IN_HEX")

if message is None or not message.strip():
    raise ValueError(
        "LOGIN_MESSAGE_IN_HEX is not set. Add it to your .env file "
        "(copy the hex string from login_messages.txt)."
    )

CLIENT_LOGIN_MESSAGE_IN_HEX: str = message.strip()

try:
    CLIENT_LOGIN_MESSAGE_IN_BYTES: bytes = bytes.fromhex(CLIENT_LOGIN_MESSAGE_IN_HEX)
except ValueError as e:
    raise ValueError(
        "LOGIN_MESSAGE_IN_HEX is not a valid hex string. "
        "Make sure you copied the whole line from login_messages.txt without extra characters."
    ) from e