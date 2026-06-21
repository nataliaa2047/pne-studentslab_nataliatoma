from Seq0 import *

print("-----| Exercise 7 |-----")

FILENAME_1 = "U5.txt"
FILENAME_2 = "ADA.txt"
FILENAME_3 = "FRAT1.txt"
FILENAME_4 = "FXN.txt"

FOLDER = "sequences/"

filename_1 = FOLDER + FILENAME_1
filename_2 = FOLDER + FILENAME_2
filename_3 = FOLDER + FILENAME_3
filename_4 = FOLDER + FILENAME_4

sequence_1 = seq_read_fasta(filename_1)
sequence_2 = seq_read_fasta(filename_2)
sequence_3 = seq_read_fasta(filename_3)
sequence_4 = seq_read_fasta(filename_4)

print(f"Gene U5: Most frequent base: {most_frequent(sequence_1)}")
print(f"Gene ADA: Most frequent base: {most_frequent(sequence_2)}")
print(f"Gene FRAT1: Most frequent base: {most_frequent(sequence_3)}")
print(f"Gene FXN: Most frequent base: {most_frequent(sequence_4,)}")