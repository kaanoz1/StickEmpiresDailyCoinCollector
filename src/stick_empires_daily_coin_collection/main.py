import socket
from socket import socket as SocketClass
import time  
from stick_empires_daily_coin_collection import PreviousStateReader
from utils import SERVER_IP, PORT, CLIENT_LOGIN_MESSAGE_IN_HEX, CLIENT_LOGIN_MESSAGE_IN_BYTES


def get_previous_coin() -> int:
    try:
        with open("previous_coin.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def save_current_coin(amount: int) -> None:
    with open("previous_coin.txt", "w") as f:
        f.write(str(amount))





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
                amount_in_bytes = mes[index + length + 1:index+length+5]
                amount_as_int = int.from_bytes(amount_in_bytes, byteorder="big")
                get_previous_coin_amount = PreviousStateReader.read_previous_state()
                diff = amount_as_int - get_previous_coin_amount
                if diff == 0:
                    print(f"No change in coin amount. Value: {amount_as_int}")
                    break

                print(f"Previous coin: {get_previous_coin_amount}, Current coin: {amount_as_int}, Diff: {diff}")
                PreviousStateReader.save_current_state(amount_as_int)
                print(f"Saved current coin amount: {amount_as_int}")

                
                print(amount_as_int)
                break


    else:
        print("FS_NEW_LOGIN_NAME couldnt found")

    
    
except Exception as e:
    print(str(e))
finally:
    client.close()


