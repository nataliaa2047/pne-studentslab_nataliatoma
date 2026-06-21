from Seq0 import *

print("-----| Exercise 7 |-----")

FILENAME = "U5.txt"
FOLDER = "sequences/"

filename = FOLDER + FILENAME

sequence = seq_read_fasta(filename)

fragment = sequence[:20]

print("Gene U5:")
print(f"Frag: {fragment}")
print(f"Comp: {seq_complement(fragment)}")