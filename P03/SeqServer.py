import socket
import os

class Seq:
    def __init__(self, str_seq=""):
        self.str_seq = str_seq

    def get_info(self):
        length = len(self.str_seq)
        if length == 0: return "Empty"
        res = f"Sequence: {self.str_seq}\nTotal length: {length}\n"
        for base in ['A', 'C', 'G', 'T']:
            count = self.str_seq.count(base)
            perc = (count / length) * 100
            res += f"{base}: {count} ({perc:.1f}%)\n"
        return res

    def get_complement(self):
        table = str.maketrans("ATCG", "TAGC")
        return self.str_seq.translate(table)

    def get_reverse(self):
        return self.str_seq[::-1]

    def read_from_file(self, gene_name):
        filename = f"sequences/{gene_name}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read().strip()
                # Skip the first line and join the rest (handles multi-line sequences)
                lines = content.split("\n")[1:]
                self.str_seq = "".join(lines).replace(" ", "")
            return True
        return False


# Exercise 2: Sequence list for GET command
GENE_LIST = [
    "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA",
    "CCCTAGCCTGACTCCCTTTCCCTTTCCATCCTCACCAGACGCCCGGCATGCCGGACCTCAAA",
    "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCTAATCTCCGTACAAAT",
    "GATTACA_SEQ_3",
    "TTAGGG_SEQ_4"
]

def start_server(host="127.0.0.1", port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("SEQ Server configured!")

    try:
        while True:  # Keep server running sequentially
            print("Waiting for clients....")
            client_socket, client_address = server_socket.accept()

            with client_socket:
                data = client_socket.recv(2048).decode("utf-8").strip()
                if not data: continue

                parts = data.split()
                command = parts[0].upper()
                response = ""

                if command == "PING":
                    print("\033[92mPING command!\033[0m")
                    response = "OK!\n"

                elif command == "GET" and len(parts) == 2:
                    idx = int(parts[1])
                    if 0 <= idx < len(GENE_LIST):
                        print("\033[92mGET\033[0m")
                        response = GENE_LIST[idx] + "\n"
                    else:
                        response = "Error: Index out of range\n"

                elif command == "INFO" and len(parts) == 2:
                    s = Seq(parts[1])
                    print("\033[92mINFO\033[0m\nNew sequence created!")
                    response = s.get_info()

                elif command == "COMP" and len(parts) == 2:
                    s = Seq(parts[1])
                    print("\033[92mCOMP\033[0m\nNew sequence created!")
                    response = s.get_complement() + "\n"

                elif command == "REV" and len(parts) == 2:
                    s = Seq(parts[1])
                    print("\033[92mREV\033[0m\nNew sequence created!")
                    response = s.get_reverse() + "\n"

                elif command == "GENE" and len(parts) == 2:
                    s = Seq()  # NULL Seq created
                    print("\033[92mGENE\033[0m\nNULL Seq created")
                    if s.read_from_file(parts[1]):
                        response = s.str_seq + "\n"
                    else:
                        response = "Error: Gene not found\n"

                else:
                    response = "Error: Unknown command\n"

                # Final Send and Console Log
                client_socket.sendall(response.encode("utf-8"))
                print(response, end="")

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    if not os.path.exists("sequences"):
        os.makedirs("sequences")
    start_server()