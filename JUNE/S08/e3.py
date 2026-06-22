import socket

# SERVER IP, PORT
def client():
    PORT = 8081
    IP = "127.0.0.1" # we use this IP when both the client and the server are in the same device

    while True:

  # -- Ask the user for the message
        message = input("Enter your message (type 'exit' to stop sending messages): ")
        if message == "exit":
            return      #the return will stop us from being asked to write another message
  # -- Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # -- Establish the connection to the Server
        s.connect((IP, PORT))
  # -- Send the user message
        s.send(str.encode(message))
  # -- Receive data from the server
        msg = s.recv(2048)
        print("MESSAGE FROM THE SERVER:\n")
        print(msg.decode("utf-8"))
  # -- Close the socket
        s.close()

client()




