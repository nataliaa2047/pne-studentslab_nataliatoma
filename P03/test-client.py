import socket


class Client:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port

    def talk(self, message):
        """Sends a message to the server and returns the response."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(message.encode("utf-8"))
                # Receive response (using a larger buffer for long gene sequences)
                response = s.recv(16384).decode("utf-8")
                return response
        except ConnectionRefusedError:
            return "Error: Server is not running."


def run_test():
    c = Client()

    print("-----| Practice 3, Exercise 7 |------")
    print(f"Connection to SERVER at 127.0.0.1, PORT: 8080")

    # 1. Testing PING
    print("\n* Testing PING...")
    print(c.talk("PING"), end="")

    # 2. Testing GET (0 to 4)
    print("\n* Testing GET...")
    sequences = []
    for i in range(5):
        seq = c.talk(f"GET {i}").strip()
        sequences.append(seq)
        print(f"GET {i}: {seq}")

    # Use GET 0 for the following tests as requested
    base_seq = sequences[0]

    # 3. Testing INFO
    print("\n* Testing INFO...")
    print(c.talk(f"INFO {base_seq}"), end="")

    # 4. Testing COMP
    print("\n* Testing COMP...")
    print(f"COMP {base_seq}")
    print(c.talk(f"COMP {base_seq}"), end="")

    # 5. Testing REV
    print("\n* Testing REV...")
    print(f"REV {base_seq}")
    print(c.talk(f"REV {base_seq}"), end="")

    # 6. Testing GENE
    print("\n* Testing GENE...")
    genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
    for gene in genes:
        print(f"GENE {gene}")
        response = c.talk(f"GENE {gene}").strip()
        # Show first 120 chars and then [...] if it's long, to match your screenshot style
        if len(response) > 120:
            print(f"{response[:120]}[...]{response[-15:]}")
        else:
            print(response)


if __name__ == "__main__":
    run_test()