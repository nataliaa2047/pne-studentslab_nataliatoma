from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "127.0.0.1" # your IP address
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)
print(c)

genes = ["U5", "FRAT1", "ADA"]

for gene_name in genes:
    s = Seq()    #we create the Seq object
    s.read_fasta(f"sequences/{gene_name}.txt")  #we open the file
    msg_announcement = f"Sending {gene_name} Gene to the server..."  #lines 22-25: we send the announcement message to the server
    print("To Server:", msg_announcement)
    response1 = c.talk(msg_announcement)
    print(f"From Server:\n{response1}\n")
    sequence_str = str(s)              #lines 26-29: we send the DNA sequence to the server
    print("To Server:", sequence_str)
    response2 = c.talk(sequence_str)
    print(f"From Server:\n{response2}\n")

