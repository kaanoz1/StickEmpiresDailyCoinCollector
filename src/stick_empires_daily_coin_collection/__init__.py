import socket
from socket import socket as SocketClass  

SERVER_IP: str = "23.23.246.201"
PORT: int = 9933

client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
try:
    client.connect((SERVER_IP, PORT))
    print("Connected")

except Exception as e:
    print(str(e))
finally:
    client.close()



