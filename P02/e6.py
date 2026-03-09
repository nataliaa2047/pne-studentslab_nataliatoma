from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 6

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "127.0.0.1" # your IP address
PORT1 = 8080
PORT2 = 8081

# -- Create a client object
c1 = Client(IP, PORT1)
c2 = Client(IP, PORT2)

print(c1)
print(c2)

gene_name = "sequences/FRAT1.txt"
s = Seq()    #we create the Seq object
s.read_fasta(gene_name)  #we open the file
gene = str(s)  #we transform the sequence into a string
print("Gene FRAT1:", gene[:70] + "...")

message = "Sending FRAT1 Gene to the server, in fragments of 10 bases..."
c1.talk(message)
c2.talk(message)

for i in range(10):
    fragment = gene[i*10:(i+1)*10]
    print(f"Fragment: {i+1}: {fragment}")
    message = f"Fragment: {i+1}: {fragment}"
    if (i+1) % 2 != 0:
        c1.talk(message)
    else:
        c2.talk(message)