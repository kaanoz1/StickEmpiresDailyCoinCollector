import socket
from socket import socket as SocketClass
import time  
from utils import SERVER_IP, PORT, CLIENT_LOGIN_MESSAGE_IN_HEX, CLIENT_LOGIN_MESSAGE_IN_BYTES

client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
try:
    client.connect((SERVER_IP, PORT))
    print("Connected")
    client.sendall(CLIENT_LOGIN_MESSAGE_IN_BYTES)
    print("Sent!")
    first_data = client.recv(1024)

    if b"FS_NEW_LOGIN_NAME" in first_data:
        print("FS_NEW_LOGIN_NAME found. User logged in.")


        now = time.time()
        while True:
            timeout: float = 5.0

            starting_time: float = time.time() - now
            remaining = timeout - starting_time

            if remaining <= 0:
                print("empirePoint not found, timeout.")
                break

            mes = client.recv(1024)
            if b"empirePoints" in mes:
                index: int = mes.find(b"empirePoints")
                length = "empirePoints".__len__()
                print(f"empirePoints found, index: {index}")
                amount_in_bytes = mes[index + length + 1:index+length+5]
                print(f"Should be 4: {amount_in_bytes}")
                amount_as_int = int.from_bytes(amount_in_bytes, byteorder="big")
                print(amount_as_int)
                break


    else:
        print("FS_NEW_LOGIN_NAME couldnt found")

    
    
except Exception as e:
    print(str(e))
finally:
    client.close()



