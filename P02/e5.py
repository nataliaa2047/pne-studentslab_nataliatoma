from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "127.0.0.1" # your IP address
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)
print(c)

gene_name = "sequences/FRAT1.txt"
s = Seq()    #we create the Seq object
s.read_fasta(gene_name)  #we open the file
gene = str(s)  #we transform the sequence into a string
print("Gene FRAT1:", gene[:60] + "...")

message = "Sending FRAT1 Gene to the server, in fragments of 10 bases..."
print("To Server:", message)
response = c.talk(message)
print("From Server:", response)

for i in range(5):
    fragment = gene[i*10:(i+1)*10]
    print(f"Fragment: {i+1}: {fragment}")
    message = f"Fragment: {i+1}: {fragment}"
    response = c.talk(message)