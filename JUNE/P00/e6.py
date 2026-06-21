from Seq0 import *

print("-----| Exercise 6 |-----")

FILENAME = "U5.txt"
FOLDER = "sequences/"

filename = FOLDER + FILENAME

sequence = seq_read_fasta(filename)

print("Gene U5")
print(f"Reverse: {seq_reverse(sequence, 20)}")