import socket

def main():
    host = "0.0.0.0"   # listen on all interfaces
    port = 2222        # fake SSH port (never use 22 in VM testing)
    
    print(f"[+] Starting fake SSH server on {host}:{port}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client, addr = server_socket.accept()
        print(f"[!] Connection attempt from {addr}")
        client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
        client.close()

if __name__ == "__main__":
    main()
