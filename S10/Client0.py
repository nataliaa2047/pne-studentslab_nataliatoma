import socket

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def ping(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ip, self.port))
                s.send("ping".encode("utf-8"))
                answer = s.recv(1024)
                if answer.decode("utf-8") == "pong":
                    print("OK!")
                else:
                    print("Unexpected response:", answer.decode("utf-8"))
        except Exception as e:
            print("Error:", e)

    def __str__(self):
        result = "Connection to SERVER at {}, PORT {}".format(self.ip, self.port)
        return result

    def talk(self, message):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
           s.connect((self.ip, self.port))
           s.send(str.encode(message))
           answer = s.recv(2048).decode("utf-8")
       return answer