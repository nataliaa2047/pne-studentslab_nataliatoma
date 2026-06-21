from Seq0 import *

FILENAME = "U5.txt"
FOLDER = "sequences/"
filename = FOLDER + FILENAME

print("DNA file:", FILENAME)

sequence = seq_read_fasta(filename)

print("The first 20 bases are:")
print(sequence[:20])