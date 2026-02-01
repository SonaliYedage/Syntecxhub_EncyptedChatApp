import socket
import threading
from crypto_utils import decrypt_message

HOST = '127.0.0.1'
PORT = 5000

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client_socket, address):
    print(f"Client connected: {address}")
    while True:
        try:
            encrypted_msg = client_socket.recv(1024)
            if not encrypted_msg:
                break

            message = decrypt_message(encrypted_msg)
            print(f"{address}: {message}")

            # Log message
            with open("chat_log.txt", "a") as log:
                log.write(f"{address}: {message}\n")

            broadcast(encrypted_msg, client_socket)

        except:
            break

    print(f"Client disconnected: {address}")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started on {HOST}:{PORT}")
    print("Waiting for clients...")

    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )
        thread.start()

start_server()
