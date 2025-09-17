import socket
import threading
import paramiko
import sys
import datetime

LOG_FILE = "honeypot.log"
HOST_KEY = paramiko.RSAKey.generate(2048)
HOST = "0.0.0.0"
PORT = 2222

class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_addr):
        self.client_addr = client_addr
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # Log username/password attempts
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.datetime.now()} - {self.client_addr} - username: {username}, password: {password}\n")
        return paramiko.AUTH_FAILED  # never allow login

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def handle_connection(client, addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = SSHServer(addr)
    try:
        transport.start_server(server=server)
        # Wait for auth attempts (but we deny all)
        transport.accept(20)
    except Exception as e:
        print(f"[!] Exception from {addr}: {e}")
    finally:
        transport.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)
    print(f"[+] Paramiko SSH honeypot listening on {HOST}:{PORT}")
    
    while True:
        client, addr = sock.accept()
        print(f"[!] Connection attempt from {addr}")
        t = threading.Thread(target=handle_connection, args=(client, addr))
        t.start()

if __name__ == "__main__":
    main()
