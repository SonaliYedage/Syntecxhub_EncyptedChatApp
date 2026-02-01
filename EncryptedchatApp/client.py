import socket
import threading
from crypto_utils import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("Connected to server")

def receive_messages():
    while True:
        try:
            encrypted_msg = client.recv(1024)
            message = decrypt_message(encrypted_msg)
            print("\nMessage:", message)
        except:
            break

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    msg = input("Enter message: ")
    encrypted = encrypt_message(msg)
    client.send(encrypted)
