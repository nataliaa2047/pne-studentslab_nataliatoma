from Client0 import Client
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

client = Client(SERVER_IP, SERVER_PORT)
for i in range(5):
    message = f"message {i}"
    response = client.talk(message)
    print(f"Sent: {message} | received: {response}")


