import socket
from stick_empires_daily_coin_collection.utils import CLIENT_LOGIN_MESSAGE_IN_BYTES
from stick_empires_daily_coin_collection.utils import SERVER_IP, PORT


class StickEmpiresServerConnector:
    def __init__(self, server_ip: str = SERVER_IP, port: int = PORT):
        self.server_ip = server_ip
        self.port = port
        self.client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_login_message(self):
        try:
            self.client.sendall(CLIENT_LOGIN_MESSAGE_IN_BYTES)
        except Exception as e:
            print(f"Error sending login message: {e}")
            raise


    def connect(self):
        try:
            self.client.connect((self.server_ip, self.port))
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise

    def get_next_message(self, buffer_size: int = 10240) -> bytes:
        try:
            return self.client.recv(buffer_size)
        except Exception as e:
            print(f"Error receiving message: {e}")
            raise

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
            raise