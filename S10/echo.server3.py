import socket
from termcolor import colored

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configure the Server's IP and PORT
PORT = 8080
IP = "127.0.0.1"

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

print("The server is configured!")

client_list = []

while True:
    # -- Waits for a client to connect
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()

    # -- Server stopped manually
    except KeyboardInterrupt:
        print("Server stopped by the user")

    client_list.append(client_ip_port)
    print(f"A client has connected frpm {client_ip_port} (Total connections: {len(client_list)})")

    try:
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode().strip()
    print(colored(f"Message received: {msg}", "green"))
    response = f"ECHO: {msg}"\n
    cs.send(response.encode())

    cs.close()

    if len(client_list) >= 5:
        print("Client connection summary:")
        for i, (ip, port) in enumerate(client_list, start=1):
            print(f" {i}, IP: {ip}, POrt: {port}")
            print("Server shutting down after 5 connections.")
            ls.close()
            exit()