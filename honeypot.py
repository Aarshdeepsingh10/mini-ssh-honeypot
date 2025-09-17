#!/usr/bin/env python3
import socket
import threading
import datetime

LOG_FILE = "honeypot.log"
HOST = "0.0.0.0"   # listen on all interfaces
PORT = 2222        # fake SSH port (never use 22)

# Function to handle each client connection
def handle_client(client, addr):
    print(f"[!] Connection attempt from {addr}")

    try:
        # Send fake SSH banner
        client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")

        # Receive first message from client
        data = client.recv(1024)
        if data:
            # Log initial client data (often username attempt)
            print(f"[!] Received from {addr}: {data}")
            with open(LOG_FILE, "a") as f:
                f.write(f"{datetime.datetime.now()} - {addr} - {data}\n")

        # Send fake password prompt (optional)
        client.send(b"Password: ")
        password = client.recv(1024)
        if password:
            print(f"[!] Password attempt from {addr}: {password}")
            with open(LOG_FILE, "a") as f:
                f.write(f"{datetime.datetime.now()} - {addr} - password: {password}\n")

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        client.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[+] Starting fake SSH server on {HOST}:{PORT}")

    while True:
        client, addr = server_socket.accept()
        # Handle each client in a separate thread
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    main()